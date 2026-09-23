# Description

For the named backend `$name`: Dead-data size in any one Bitcask file that triggers a merge attempt. Lower values trigger earlier, more frequent merges; the separate merge thresholds determine which files participate. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: bitcask
repository: bitcask
module: bitcask_multi.schema
concept: compaction, storage

# Reviewed against

3.4.0: 43f8f2bb43784f3c5615b032c81496deaa06b5f5428396f8d33965da26ba0a03
3.4.1: 43f8f2bb43784f3c5615b032c81496deaa06b5f5428396f8d33965da26ba0a03
