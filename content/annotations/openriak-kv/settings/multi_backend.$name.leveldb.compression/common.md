# Description

For the named backend `$name`: Enable compression for newly written or compacted LevelDB data. Changing it does not rewrite existing files immediately; the space and I/O effects appear as files are replaced through normal compaction. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb_multi.schema
concept: compression, storage

# Reviewed against

3.4.0: 79e3df2ec05aa693e8c736f3758d57c51dc97b31df81e5eab96d4e2fc4d32beb
3.4.1: 79e3df2ec05aa693e8c736f3758d57c51dc97b31df81e5eab96d4e2fc4d32beb
