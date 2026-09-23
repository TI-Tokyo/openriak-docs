# Description

For the named backend `$name`: Ending hour of the permitted Bitcask merge window, used when `bitcask.merge.policy = window`. Pair it with `.start`; the hour is expressed on the 0–23 clock. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: bitcask
repository: bitcask
module: bitcask_multi.schema
concept: compaction, storage

# Reviewed against

3.4.0: e3353381864c2f3e5dba3657710a5c2efbe0f8298c1ed3f20b6430c0eaa20d01
3.4.1: e3353381864c2f3e5dba3657710a5c2efbe0f8298c1ed3f20b6430c0eaa20d01
