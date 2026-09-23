# Description

Number of delete tombstones in one SST file that can trigger background compaction by itself. Use `off` to disable this extra trigger; ordinary compaction still follows the backend's other rules.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb.schema
concept: compaction, storage

# Reviewed against

3.4.0: 43f256a32332a258fa94562fd9b31af906177d91fd566f344e008d8bb4126258
3.4.1: 43f256a32332a258fa94562fd9b31af906177d91fd566f344e008d8bb4126258
