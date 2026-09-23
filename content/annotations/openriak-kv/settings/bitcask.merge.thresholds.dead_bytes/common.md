# Description

Minimum dead-data size for including a file in an already-triggered Bitcask merge. Lowering it includes more files. This selects merge inputs; `bitcask.merge.triggers.dead_bytes` controls when a merge starts.

# Tags

feature: bitcask
repository: bitcask
module: bitcask.schema
concept: compaction, storage

# Reviewed against

3.4.0: f1f44ea73c1b7c54ed2e703e1fcb8cca9d7b8039d27e9b59ffb2836ade4dbf30
3.4.1: f1f44ea73c1b7c54ed2e703e1fcb8cca9d7b8039d27e9b59ffb2836ade4dbf30
