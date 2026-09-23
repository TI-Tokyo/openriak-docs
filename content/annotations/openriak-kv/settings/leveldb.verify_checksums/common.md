# Description

Verify internal checksums when reading LevelDB data. Disabling this removes a corruption-detection check from reads; it is separate from verification during compaction.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb.schema
concept: storage

# Reviewed against

3.4.0: 789202de7bf9002c556b3c44f382872e06a86b17cf626d7cf283fd9880315e06
3.4.1: 789202de7bf9002c556b3c44f382872e06a86b17cf626d7cf283fd9880315e06
