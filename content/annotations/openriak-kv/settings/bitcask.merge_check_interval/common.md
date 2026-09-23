# Description

Interval between checks for Bitcask files needing a merge. Merge policy and trigger thresholds still determine whether work starts; this interval only controls how often eligibility is checked.

# Tags

feature: bitcask
repository: riak_kv
module: riak_kv_bitcask_backend
concept: compaction, scheduling, storage

# Reviewed against

3.4.0: db83a2dcc89591bfc33e49d6323b636daf2e18c64623984a179533ae6619770e
3.4.1: 5e1815cf3a3e55db444cdd0624282ac969e63dd4c1e17040fe6af70088094d5e
