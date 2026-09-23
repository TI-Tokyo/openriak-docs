# Description

For the named backend `$name`: Choose when journal objects are compressed: on receipt or during compaction. Deferring compression to compaction avoids immediate compression work on incoming writes; ledger compression has its own controls. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveled
repository: leveled
module: leveled_multi.schema
concept: compression, storage

# Reviewed against

3.4.0: 6a2d770aad232cd31b3ee88aa7d686ef615a6b6b48ccac2ca3ca62863e46674f
3.4.1: 371c2596f5d27586b680f684300dcbbddaad4324ce7edfb774fa81953ca7de66
