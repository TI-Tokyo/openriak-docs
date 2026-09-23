# Description

For the named backend `$name`: Dead-key percentage at which a Bitcask file becomes eligible for an already-triggered merge. Lower values include less-fragmented files, increasing merge work in exchange for earlier space reclamation. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: bitcask
repository: bitcask
module: bitcask_multi.schema
concept: compaction, storage

# Reviewed against

3.4.0: f451bd5fa99d8794c8a80ec134ec4ab8feb55b0e4f1887a9ae4cfe5e494d4d41
3.4.1: f451bd5fa99d8794c8a80ec134ec4ab8feb55b0e4f1887a9ae4cfe5e494d4d41
