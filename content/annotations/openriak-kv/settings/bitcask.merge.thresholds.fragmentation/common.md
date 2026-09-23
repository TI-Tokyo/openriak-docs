# Description

Dead-key percentage at which a Bitcask file becomes eligible for an already-triggered merge. Lower values include less-fragmented files, increasing merge work in exchange for earlier space reclamation.

# Tags

feature: bitcask
repository: bitcask
module: bitcask.schema
concept: compaction, storage

# Reviewed against

3.4.0: ef0cf631f25d3f4e2a12409d5379591da178d41130c47448469dbfe80df16b90
3.4.1: ef0cf631f25d3f4e2a12409d5379591da178d41130c47448469dbfe80df16b90
