# Description

For the named backend `$name`: Control whether LevelDB can discard an entire SST file when its contents have expired. Whole-file expiry can reclaim space without removing every expired key individually during compaction. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb_multi.schema
concept: retention, storage

# Reviewed against

3.4.0: cad107c40502888a2000026e632178c6681c5851d1d6fbb7c520d06fb56f67ae
3.4.1: cad107c40502888a2000026e632178c6681c5851d1d6fbb7c520d06fb56f67ae
