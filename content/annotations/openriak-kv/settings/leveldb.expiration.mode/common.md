# Description

Control whether LevelDB can discard an entire SST file when its contents have expired. Whole-file expiry can reclaim space without removing every expired key individually during compaction.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb.schema
concept: retention, storage

# Reviewed against

3.4.0: 8dd9f7615ea804310be7099af684c3b6cc4a62bd43eab919b22da7b293b4af0f
3.4.1: 8dd9f7615ea804310be7099af684c3b6cc4a62bd43eab919b22da7b293b4af0f
