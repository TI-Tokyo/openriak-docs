# Description

For the named backend `$name`: Additional delay before expired keys alone trigger a Bitcask merge. Increasing this reduces repeated expiry-driven merges; it delays reclaiming disk space rather than extending the configured retention period. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: bitcask
repository: bitcask
module: bitcask_multi.schema
concept: retention, storage

# Reviewed against

3.4.0: e8a52552758fd48d27700587079d9c194e8a795c8cbda0f706ed890266bbf687
3.4.1: e8a52552758fd48d27700587079d9c194e8a795c8cbda0f706ed890266bbf687
