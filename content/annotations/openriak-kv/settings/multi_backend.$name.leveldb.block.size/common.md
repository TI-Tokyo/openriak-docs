# Description

For the named backend `$name`: Target size of a data block within a LevelDB SST file. Blocks are indexed and cached separately; this is neither the SST-file size nor the database-size limit. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb_multi.schema
concept: storage

# Reviewed against

3.4.0: d1d7ea86acef8280d3535525dc1a56cfd61d77c3cf1a121fba9084b8adadc963
3.4.1: d1d7ea86acef8280d3535525dc1a56cfd61d77c3cf1a121fba9084b8adadc963
