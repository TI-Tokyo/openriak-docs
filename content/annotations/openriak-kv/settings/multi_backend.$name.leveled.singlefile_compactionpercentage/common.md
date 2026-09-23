# Description

For the named backend `$name`: Retained-data percentage below which a single journal file qualifies for compaction. Lower values require a larger fraction of reclaimable space before rewriting that file. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveled
repository: leveled
module: leveled_multi.schema
concept: compaction, storage

# Reviewed against

3.4.0: d7767661e864fedd27837c48bda2a2d3fdffaf9929a8448ff1c6453b1a824f60
3.4.1: 35f95ffcbf3fac71eb91b69fd6ca138cb82d49e45d7e885b28770d48dd972df8
