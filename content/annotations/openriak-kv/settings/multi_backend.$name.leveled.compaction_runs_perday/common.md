# Description

For the named backend `$name`: Number of journal-compaction opportunities per vnode per day. Increasing it can reclaim dead space sooner but adds background I/O and CPU work. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveled
repository: leveled
module: leveled_multi.schema
concept: compaction, storage

# Reviewed against

3.4.0: 7c0435ba8f31893ee1ccb40772d98f1fb9316a0548db668fe54eb5056e54602d
3.4.1: 78ce0101e382d88c50023166c885ee7553c8d40f7e6f31b40ab8129f2ec58a80
