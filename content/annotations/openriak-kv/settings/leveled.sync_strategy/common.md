# Description

Choose how Leveled flushes writes to disk. `none` lets the operating system schedule flushing; `sync` and `riak_sync` synchronize each PUT using their respective mechanisms. Per-write synchronization trades latency and throughput for persistence.

# Tags

feature: leveled
repository: leveled
module: leveled.schema
concept: storage

# Reviewed against

3.4.0: f8dc62be9efd8b311cdf704930a84ac544379ceaad1fcfec09e9430b890c214e
3.4.1: 1f2f4d270def2f8da55b801c16db43014f7c52ce11a960d54648a832f776f3b2
