# Description

For the named backend `$name`: Key-count capacity of Leveled's Bookie memory cache. This is a count of keys, not a byte budget; the pause threshold also depends on `leveled.cache_multiple`. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveled
repository: leveled
module: leveled_multi.schema
concept: memory, storage

# Reviewed against

3.4.0: a1b69682c9efc580deb788b434f2d3fb999a6964f7f02f93ea953dae849306b0
3.4.1: 80ce0ee37009cdc8cdf7cbb0806b7f349b7554b5e1493396b5d53a8f58479522
