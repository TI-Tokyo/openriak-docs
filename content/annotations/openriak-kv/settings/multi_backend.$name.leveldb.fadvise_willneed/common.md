# Description

For the named backend `$name`: Use the operating-system WILLNEED file-access hint instead of DONTNEED for LevelDB. It can help when physical memory can hold the database, but changes page-cache pressure for the rest of the node. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb_multi.schema
concept: storage

# Reviewed against

3.4.0: a54383c1ae2789898f0797d17d689880b3d6cf4b8d7472a163b74af9311a3457
3.4.1: a54383c1ae2789898f0797d17d689880b3d6cf4b8d7472a163b74af9311a3457
