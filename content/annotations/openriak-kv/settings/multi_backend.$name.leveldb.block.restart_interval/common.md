# Description

For the named backend `$name`: Number of keys between restart entries in a LevelDB block's key index. This changes the tradeoff between index overhead and key reconstruction during reads; most workloads should retain the default. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb_multi.schema
concept: scheduling, storage

# Reviewed against

3.4.0: 1d6b5fcd37e40ec19bcb6f6b50c6b491257f2f17aae6dcbef2158f966ab2dd11
3.4.1: 1d6b5fcd37e40ec19bcb6f6b50c6b491257f2f17aae6dcbef2158f966ab2dd11
