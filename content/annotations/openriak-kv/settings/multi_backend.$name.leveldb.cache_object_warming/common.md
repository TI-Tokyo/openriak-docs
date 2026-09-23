# Description

For the named backend `$name`: Save cache information, currently open SST filenames, when closing a database and use it on the next open. This can reduce initial request latency by reopening those files before client reads need them. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb_multi.schema
concept: memory, storage

# Reviewed against

3.4.0: 2bdfdd9f4b42867954d2314e677c76036099fb885cba4f4f572a7aff06a1e64e
3.4.1: 2bdfdd9f4b42867954d2314e677c76036099fb885cba4f4f572a7aff06a1e64e
