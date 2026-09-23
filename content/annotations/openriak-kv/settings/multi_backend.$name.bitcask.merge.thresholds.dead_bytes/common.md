# Description

For the named backend `$name`: Minimum dead-data size for including a file in an already-triggered Bitcask merge. Lowering it includes more files. This selects merge inputs; `bitcask.merge.triggers.dead_bytes` controls when a merge starts. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: bitcask
repository: bitcask
module: bitcask_multi.schema
concept: compaction, storage

# Reviewed against

3.4.0: 53941fb4b1780d2f5665815b03e2ee95f4857395e753a7042e8eee0834acd2cc
3.4.1: 53941fb4b1780d2f5665815b03e2ee95f4857395e753a7042e8eee0834acd2cc
