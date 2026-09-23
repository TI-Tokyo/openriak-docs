# Description

Reduce LevelDB memory use for development hosts running many vnodes or VMs. This overrides the minimum and maximum write-buffer settings and is unsuitable for representative performance measurements.

# Tags

feature: leveldb
repository: eleveldb, riak
module: eleveldb.schema, riak.schema
concept: storage

# Reviewed against

3.4.0: d4b981b7e8bd865536e789476fed3906fce86553b071fac243b86c964d2e3c80
3.4.1: d4b981b7e8bd865536e789476fed3906fce86553b071fac243b86c964d2e3c80
