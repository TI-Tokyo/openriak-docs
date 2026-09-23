# Description

For the named backend `$name`: Verify internal checksums when reading LevelDB data. Disabling this removes a corruption-detection check from reads; it is separate from verification during compaction. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb_multi.schema
concept: storage

# Reviewed against

3.4.0: cace32f86aa0e9b4396a3c1b4a8be7d3383e9b65328d1922670cdf7ff800f663
3.4.1: cace32f86aa0e9b4396a3c1b4a8be7d3383e9b65328d1922670cdf7ff800f663
