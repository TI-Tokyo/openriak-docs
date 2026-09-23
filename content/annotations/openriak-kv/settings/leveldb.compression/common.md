# Description

Enable compression for newly written or compacted LevelDB data. Changing it does not rewrite existing files immediately; the space and I/O effects appear as files are replaced through normal compaction.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb.schema
concept: compression, storage

# Reviewed against

3.4.0: daf934a236e256389d18d8ca2fd4e6bbf78488f7558fd5753f8afa1e3b95878d
3.4.1: daf934a236e256389d18d8ca2fd4e6bbf78488f7558fd5753f8afa1e3b95878d
