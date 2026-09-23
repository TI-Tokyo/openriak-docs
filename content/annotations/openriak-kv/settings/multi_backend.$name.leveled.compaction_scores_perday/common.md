# Description

For the named backend `$name`: How often each journal file is assessed for compaction over a day. More frequent scoring discovers reclaimable space sooner, at the cost of extra background assessment work. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveled
repository: leveled
module: leveled_multi.schema
concept: compaction, storage

# Reviewed against

3.4.0: 96482b7bb48306a81a0d7aced112c8e757754ccfe6e96a44717f638bae94ebab
3.4.1: e721b9a0ff75efd88b79276dda72e9ebbbc29a25afbe849c2db759b90e657585
