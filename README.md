#ploopsnapshot

A small Python package that can create and track snapshots created by Ploop.  Tracking is done via sqlite entries, using the snapshot name as a primary key.

###Usage

#### `ploopSnapshot(ctid, datadir = '.', ddxml=None)`

  Creates a new ploopSnapshot 'object'.

  * `ctid` - the OpenVZ containter ID to work with
  * `datadir` - the directory to create/look for the database in
  * `ddxml` - the location of the DiskDescriptor.xml for the container

#### `getSnapshots()`

  Returns a dictionary of snapshots, with name as key and uuid as element.

#### `createSnapshot(uuid=None)`

  Creates a snapshot via the ploop command, and returns the status code.

  * `uuid` - the UUID to use for the snapshot. if not provided, one is generated via uuid4().

#### `deleteSnapshot(uuid=None)`

  Deletes a snapshot via the ploop command, and returns the status code.

#### `createDB()`

  Creates a new sqlite database with the appropiate schema.

#### `updateDB(name, uuid, method = "insert")`

  Changes or adds content to the database based on passed method. Default is insert.

  * `name` - the unique name to identify the snapshot
  * `uuid` - the UUID for the snapshot
  * `method` - options are `insert` or `update`. defaults to insert to not unknowingly overwrite data if existing name is used

###DailyPloop

Included is a script called `dailyploop`.  This script will manage daily snapshots of a Ploop device, given a container ID.  It can be used as is, or as an example of how to work with the module.
