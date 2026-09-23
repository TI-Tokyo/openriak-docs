# Description

For the named backend `$name`: Synchronize LevelDB's write log on each write. This improves persistence against machine failure at the cost of synchronization latency; it does not change replica quorum requirements. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb_multi.schema
concept: storage

# Reviewed against

3.4.0: ac2666c279ebac983ccfb5497a146f2eb4ca253ff4582077b186dcbf21356514
3.4.1: ac2666c279ebac983ccfb5497a146f2eb4ca253ff4582077b186dcbf21356514
