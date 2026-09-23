# Description

For the named backend `$name`: Lower bound of the randomly selected per-vnode LevelDB write-buffer size. New values enter this memory buffer alongside the recovery log before being flushed into SST files. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb_multi.schema
concept: memory, storage

# Reviewed against

3.4.0: c266149a8c70b33adca3a601e88590dd653f75e25710ea33496e7115c5949a9f
3.4.1: c266149a8c70b33adca3a601e88590dd653f75e25710ea33496e7115c5949a9f
