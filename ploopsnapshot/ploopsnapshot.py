###
# Copyright (C) 2016  Nexcess.net L.L.C.
###

import datetime
import logging
import os
import sqlite3
import subprocess
import uuid
from .schema import schema

class ploopSnapshot:
  def __init__(self, ctid, datadir = '.', ddxml=None):
    """Creates a new ploopSnapshot 'object'.

    Required arguments:
    ctid - the OpenVZ containter ID to work with

    Optional keyword arguments:
    datadir - the directory to create/look for the database in
    ddxml - the location of the DiskDescriptor.xml for the container
    """
    self.ctid = str(ctid)
    self.dbpath = ".".join(["/".join([datadir, self.ctid]), 'sqlite'])
    self.ddxml = ddxml if ddxml != None else "/vz/private/%s/root.hdd/DiskDescriptor.xml" % self.ctid
    self.log = logging.getLogger(__name__)
    if not os.path.exists(self.dbpath):
      self.createDB()
    self.db = sqlite3.connect(self.dbpath)

  def getSnapshots(self):
    """Returns a dictionary of snapshots, with name as key and uuid as element."""
    snapshots = {}
    with self.db as db:
      cur = db.cursor()
      cur.execute("""select name, uuid from snapshots""")
      for row in cur.fetchall():
        name, uuid = row
        snapshots[name] = uuid
    return snapshots

  def createSnapshot(self, uuid=None):
    """Creates a snapshot via the ploop command, and returns the status code."""
    guid = uuid if uuid else str(uuid.uuid4())
    create_snapshot_command = subprocess.Popen(["ploop", "snapshot", "-u", "{%s}" % guid, self.ddxml], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (cmd_out, _) = create_snapshot_command.communicate()
    self.log.debug(cmd_out)
    status = create_snapshot_command.returncode
    return status

  def deleteSnapshot(self, uuid):
    """Deletes a snapshot via the ploop command, and returns the status code."""
    guid = uuid
    delete_snapshot_command = subprocess.Popen(["ploop", "snapshot-delete", "-u", guid, self.ddxml], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (cmd_out, _) = delete_snapshot_command.communicate()
    self.log.debug(cmd_out)
    status = delete_snapshot_command.returncode
    return status

  def createDB(self):
    """Creates a new sqlite database with the appropiate schema."""
    self.log.info("db not found...creating db...")
    db = sqlite3.connect(self.dbpath)
    db.executescript(schema)
    db.close()

  def updateDB(self, name, uuid, method = "insert"):
    """Changes or adds content to the database based on passed method. Default is insert."""
    sname = name
    guid = uuid
    utype = method
    timestamp = datetime.datetime.now().isoformat()
    if utype == "insert":
      with self.db as db:
        db.execute("""
        insert into snapshots (name, uuid, created_at) values (?, ?, ?)""", (sname, guid, timestamp))
    elif utype == "update":
      with self.db as db:
        db.execute("""
        update snapshots set uuid = ?, created_at = ? where name = ?""", (guid, timestamp, sname))
    else:
      self.log.error("invalid method passed")

  def __del__(self):
    """Close the db connection when the ploopSnapshot object is removed."""
    self.db.close()

