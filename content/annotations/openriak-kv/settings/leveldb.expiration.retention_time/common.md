# Description

Retention period, in minutes, before stored LevelDB values expire. `unlimited` disables age-based expiry. This backend policy is separate from tombstone retention after explicit deletes.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb.schema
concept: retention, storage

# Reviewed against

3.4.0: 65b4d37bdaef893513a0a466a3cc2335074952b81796b2e004da145b86cc9333
3.4.1: 65b4d37bdaef893513a0a466a3cc2335074952b81796b2e004da145b86cc9333
