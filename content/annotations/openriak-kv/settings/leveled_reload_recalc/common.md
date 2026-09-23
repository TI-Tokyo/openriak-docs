# Description

Use Leveled's `recalc` compaction/reload strategy to discard obsolete key-change history. This saves journal space but adds index recalculation during reload. Reverting to `retain` requires rebuilding data on replacement nodes; simply reverting the setting is insufficient.

# Tags

feature: leveled
repository: riak_kv
module: riak_kv_leveled_backend
concept: storage

# Reviewed against

3.4.0: cbf643826f5da454c49fbca0ee8896d0289450cb6c238206a0c7d30a3df8ad3f
3.4.1: 099b0f7c9b6aaa6bf14378303105211302e788b9e91114dc754d081c96286df0
