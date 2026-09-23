# Description

For the named backend `$name`: Interval between disk synchronization operations when `bitcask.sync.strategy = interval`. Shorter intervals reduce the unsynchronized-write window but increase synchronization I/O. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: bitcask
repository: bitcask
module: bitcask_multi.schema
concept: scheduling, storage

# Reviewed against

3.4.0: ac0bfd3d2024bd67dea0187ece31ad7026ddeab119228ddf54b9b18121c3179b
3.4.1: ac0bfd3d2024bd67dea0187ece31ad7026ddeab119228ddf54b9b18121c3179b
