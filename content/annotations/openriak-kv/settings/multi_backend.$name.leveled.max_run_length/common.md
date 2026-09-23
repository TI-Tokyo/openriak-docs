# Description

For the named backend `$name`: Maximum number of consecutive journal files considered in one Leveled compaction run. Evaluate it together with the single-file and maximum-run compaction percentages, which determine whether a candidate is worthwhile. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveled
repository: leveled
module: leveled_multi.schema
concept: storage

# Reviewed against

3.4.0: fbb51364f18702cf0b75f3ff234fbe7b116c19f8d47a38c769c824492fddd085
3.4.1: 0746d65a333ff0e88a6032b01768d6b332e1b13fd5164e52e122e3662c3f98bc
