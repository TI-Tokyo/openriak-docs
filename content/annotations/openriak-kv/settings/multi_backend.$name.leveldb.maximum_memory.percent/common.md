# Description

For the named backend `$name`: Percentage of host memory assigned to LevelDB's dynamically sized caches. Use `leveldb.maximum_memory` for an absolute budget; leave capacity for the VM, other backends and the operating-system page cache. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb_multi.schema
concept: memory, storage

# Reviewed against

3.4.0: c168261462c8477c09ff7c15d59619eea616c3135f8d0def2e8291435de3c4b6
3.4.1: c168261462c8477c09ff7c15d59619eea616c3135f8d0def2e8291435de3c4b6
