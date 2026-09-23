# Description

For the named backend `$name`: Compression codec used by LevelDB when compression is enabled. Choose among the reported supported values and measure the space-versus-CPU tradeoff for your data. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb_multi.schema
concept: compression, storage

# Reviewed against

3.4.0: 3982573763d4342824ebd32396a312eddfd157af7e82b540617b5f0d85b5e1e3
3.4.1: 3982573763d4342824ebd32396a312eddfd157af7e82b540617b5f0d85b5e1e3
