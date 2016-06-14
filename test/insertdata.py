###
# Copyright (C) 2016  Nexcess.net L.L.C.
###

## quick script to insert data into sqlite db for testing
import sqlite3
import datetime
import sys
from uuid import uuid4

dows = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

for day in dows:
  uid = str(uuid4())
  create = datetime.datetime.now().isoformat()
  with sqlite3.connect(sys.argv[1]) as s:
    s.execute("insert into snapshots (name, uuid, created_at) values (?, ?, ?)", (day, uid, create))
