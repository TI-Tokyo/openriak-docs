# Description

For the named backend `$name`: Number of delete tombstones in one SST file that can trigger background compaction by itself. Use `off` to disable this extra trigger; ordinary compaction still follows the backend's other rules. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb_multi.schema
concept: compaction, storage

# Reviewed against

3.4.0: 51fa0a959645fb5b6e750d3f2bc58e1f9d3e89d11165e0c86f7153c97990e5d5
3.4.1: 51fa0a959645fb5b6e750d3f2bc58e1f9d3e89d11165e0c86f7153c97990e5d5
