# Description

For the named backend `$name`: Node memory budget for LevelDB's dynamically sized caches, expressed as a byte size. `leveldb.maximum_memory.percent` provides percentage-based sizing instead; this is not a limit on the whole Erlang VM. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb_multi.schema
concept: memory, storage

# Reviewed against

3.4.0: 432298c64b632ca2e6402b335066ee7e3b28fcaa0653f69377a464268dfc07b2
3.4.1: 432298c64b632ca2e6402b335066ee7e3b28fcaa0653f69377a464268dfc07b2
