# Description

Per-vnode block-cache threshold below which memory is not released in favour of the operating-system page cache. It does not prevent memory being reassigned to the LevelDB file cache.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb.schema
concept: memory, storage

# Reviewed against

3.4.0: 6be8c953ba156620ba44c50d6572908cc1cd95f74edf3f713d68ae709df483d3
3.4.1: 6be8c953ba156620ba44c50d6572908cc1cd95f74edf3f713d68ae709df483d3
