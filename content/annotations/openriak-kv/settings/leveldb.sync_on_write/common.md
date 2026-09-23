# Description

Synchronize LevelDB's write log on each write. This improves persistence against machine failure at the cost of synchronization latency; it does not change replica quorum requirements.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb.schema
concept: storage

# Reviewed against

3.4.0: e55f9f9846efc336cb6f4d286c29f7c49a81e720f789900bfaf705bdd75c7e22
3.4.1: e55f9f9846efc336cb6f4d286c29f7c49a81e720f789900bfaf705bdd75c7e22
