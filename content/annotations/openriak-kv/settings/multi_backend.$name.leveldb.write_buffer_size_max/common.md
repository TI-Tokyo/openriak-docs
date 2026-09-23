# Description

For the named backend `$name`: Upper bound of the randomly selected per-vnode LevelDB write-buffer size. Used with `.write_buffer_size_min` to spread flush activity; larger buffers increase aggregate memory demand across vnodes. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb_multi.schema
concept: memory, storage

# Reviewed against

3.4.0: d0afc15d4cad3e75c44698d7e883d5480d61692216e96fc6a6ca64bc3a2e1487
3.4.1: d0afc15d4cad3e75c44698d7e883d5480d61692216e96fc6a6ca64bc3a2e1487
