# Description

For the named backend `$name`: Starting hour of the permitted Bitcask merge window, used when `bitcask.merge.policy = window`. Pair it with `.end` to move merge activity into the desired daily period. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: bitcask
repository: bitcask
module: bitcask_multi.schema
concept: compaction, storage

# Reviewed against

3.4.0: ff512e21225933290b236b1941d36ecf23787bbf80e5e78a6099bd432504f516
3.4.1: ff512e21225933290b236b1941d36ecf23787bbf80e5e78a6099bd432504f516
