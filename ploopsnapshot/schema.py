###
# Copyright (C) 2016  Nexcess.net L.L.C.
###

# this is simply the schema to use when createing a new db
schema = """
create table snapshots (
    name         text primary key not null,
    uuid         text,
    created_at   date
);"""
