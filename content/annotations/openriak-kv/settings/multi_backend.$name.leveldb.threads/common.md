# Description

For the named backend `$name`: Number of native worker threads used for LevelDB operations. More threads permit more concurrent backend work but do not remove storage or CPU bottlenecks. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb_multi.schema
concept: concurrency, storage

# Reviewed against

3.4.0: 44859a61e26a95a35837d4909bb6bbe26324344a3edbbd31d396ca66a3a80aa1
3.4.1: 44859a61e26a95a35837d4909bb6bbe26324344a3edbbd31d396ca66a3a80aa1
