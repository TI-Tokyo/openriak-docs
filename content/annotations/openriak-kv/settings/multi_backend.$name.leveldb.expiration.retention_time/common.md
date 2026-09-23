# Description

For the named backend `$name`: Retention period, in minutes, before stored LevelDB values expire. `unlimited` disables age-based expiry. This backend policy is separate from tombstone retention after explicit deletes. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb_multi.schema
concept: retention, storage

# Reviewed against

3.4.0: bb5c5a75c8c395e444c64b6fb82fff7b19013941e8c43272fcf36ffbc9e4f3f6
3.4.1: bb5c5a75c8c395e444c64b6fb82fff7b19013941e8c43272fcf36ffbc9e4f3f6
