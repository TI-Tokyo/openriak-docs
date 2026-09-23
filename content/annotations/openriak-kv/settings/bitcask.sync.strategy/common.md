# Description

Choose when Bitcask synchronizes writes to disk. `none` relies on operating-system flushing, `o_sync` requests synchronous writes, and `interval` uses `bitcask.sync.interval`. This changes durability against machine or power failure as well as write latency.

# Tags

feature: bitcask
repository: bitcask
module: riak_kv_bitcask_backend
concept: storage

# Reviewed against

3.4.0: 5f60d5038316b6a3af2c888cdf5a7bea1127ba18aa27782e52560770f0f892ae
3.4.1: 5f60d5038316b6a3af2c888cdf5a7bea1127ba18aa27782e52560770f0f892ae
