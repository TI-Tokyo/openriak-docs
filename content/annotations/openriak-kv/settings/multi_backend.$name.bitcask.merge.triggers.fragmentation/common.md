# Description

For the named backend `$name`: Dead-key percentage in a Bitcask file that triggers a merge attempt. The trigger starts merge selection; the `bitcask.merge.thresholds.*` settings govern which files are included. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: bitcask
repository: bitcask
module: bitcask_multi.schema
concept: compaction, storage

# Reviewed against

3.4.0: 7d9779125715d3e617cb327ef90eaa3e66cb04bf99eb9fc4f07b899a78cf577d
3.4.1: 7d9779125715d3e617cb327ef90eaa3e66cb04bf99eb9fc4f07b899a78cf577d
