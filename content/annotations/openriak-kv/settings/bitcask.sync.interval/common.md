# Description

Interval between disk synchronization operations when `bitcask.sync.strategy = interval`. Shorter intervals reduce the unsynchronized-write window but increase synchronization I/O.

# Tags

feature: bitcask
repository: bitcask
module: riak_kv_bitcask_backend
concept: scheduling, storage

# Reviewed against

3.4.0: 7707ab65935f8debc2bedffe9936001d9ddc4dc4b5dd109cc55e4f99611db350
3.4.1: 7707ab65935f8debc2bedffe9936001d9ddc4dc4b5dd109cc55e4f99611db350
