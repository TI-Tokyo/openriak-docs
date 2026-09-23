# Description

For the named backend `$name`: First local-clock hour when Leveled journal compaction may run. Pair it with `leveled.compaction_top_hour`; 0 through 23 allows work throughout the day. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveled
repository: leveled
module: leveled_multi.schema
concept: compaction, storage

# Reviewed against

3.4.0: 92372be1cc93993845ae8bbe3a6c2f3a4c6c2008c9a23feb90b9a147bd14488d
3.4.1: e3c34b90277293d0433cc05e1f90594a79c824bc58e1cbde3672c449b8c0606f
