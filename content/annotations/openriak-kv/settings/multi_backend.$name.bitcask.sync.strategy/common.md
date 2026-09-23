# Description

For the named backend `$name`: Choose when Bitcask synchronizes writes to disk. `none` relies on operating-system flushing, `o_sync` requests synchronous writes, and `interval` uses `bitcask.sync.interval`. This changes durability against machine or power failure as well as write latency. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: bitcask
repository: bitcask
module: bitcask_multi.schema
concept: storage

# Reviewed against

3.4.0: 2634f6163f938c86cefd9200475c2211d09962f613c39d6d031dc8b94f39630f
3.4.1: 2634f6163f938c86cefd9200475c2211d09962f613c39d6d031dc8b94f39630f
