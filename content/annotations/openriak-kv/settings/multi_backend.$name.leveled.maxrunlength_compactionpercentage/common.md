# Description

For the named backend `$name`: Retained-data percentage below which a maximum-length journal run qualifies for compaction. A lower value demands more reclaimable space before the run is selected. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveled
repository: leveled
module: leveled_multi.schema
concept: compaction, storage

# Reviewed against

3.4.0: 241d9a2aac74d069149baaca572f021439a8895e551400f3e2cc7e7638413ad3
3.4.1: 7cf5f85328edb6d8cba036f5af8a00bc7dcd18ffd2fd1974142fe9ad678e72a9
