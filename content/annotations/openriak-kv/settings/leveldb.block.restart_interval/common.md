# Description

Number of keys between restart entries in a LevelDB block's key index. This changes the tradeoff between index overhead and key reconstruction during reads; most workloads should retain the default.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb.schema
concept: scheduling, storage

# Reviewed against

3.4.0: c9880b95f6a4417df775c9474121272cc6ade0197b4fccaefdad7bab993acbee
3.4.1: c9880b95f6a4417df775c9474121272cc6ade0197b4fccaefdad7bab993acbee
