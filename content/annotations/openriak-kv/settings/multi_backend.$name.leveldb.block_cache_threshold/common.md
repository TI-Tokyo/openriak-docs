# Description

For the named backend `$name`: Per-vnode block-cache threshold below which memory is not released in favour of the operating-system page cache. It does not prevent memory being reassigned to the LevelDB file cache. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb_multi.schema
concept: memory, storage

# Reviewed against

3.4.0: 9a460d877aa37a192a65a5b319730d96d980e5d57ca5afe7236052dc245f01a5
3.4.1: 9a460d877aa37a192a65a5b319730d96d980e5d57ca5afe7236052dc245f01a5
