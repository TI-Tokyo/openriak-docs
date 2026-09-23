# Description

For the named backend `$name`: Last local-clock hour in the Leveled compaction window, inclusive. If the starting hour exceeds this ending hour, the window crosses midnight. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveled
repository: leveled
module: leveled_multi.schema
concept: compaction, storage

# Reviewed against

3.4.0: c0a85f5288161e654853faea3f298f00bbeca71553e228f5d0c5a76abc73163a
3.4.1: c83c5391f9bcfa49eeb75b894fbcdd627409623676a743bc10fe43d36efb5275
