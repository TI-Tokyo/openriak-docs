# Description

First LevelDB level placed on the slow storage tier; lower levels use the fast tier. `off` disables tiering. Changing the split does not move existing files automatically, so existing data needs a planned migration.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb.schema
concept: storage

# Reviewed against

3.4.0: 4b7b88c51d095ef38360d632a24ae2f8823e66141da0a00462d5f079179ebfb0
3.4.1: 4b7b88c51d095ef38360d632a24ae2f8823e66141da0a00462d5f079179ebfb0
