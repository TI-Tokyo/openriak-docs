# Description

For the named backend `$name`: Reduce LevelDB memory use for development hosts running many vnodes or VMs. This overrides the minimum and maximum write-buffer settings and is unsuitable for representative performance measurements. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb_multi.schema
concept: storage

# Reviewed against

3.4.0: a41632450f473e08bc673b101bbff0187930ce99cd3d22f52173d7cea54a30d5
3.4.1: a41632450f473e08bc673b101bbff0187930ce99cd3d22f52173d7cea54a30d5
