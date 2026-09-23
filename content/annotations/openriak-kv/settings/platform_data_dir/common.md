# Description

Platform-specific root for persistent node data. Other settings may derive paths from it; ensure the service account can access the configured location and plan migration of existing files separately.

# Tags

feature: installation
repository: riak_core
module: riak_core_metadata_hashtree, riak_core_metadata_manager, riak_core_ring_manager, riak_core_sup, riak_kv_exchange_fsm, riak_kv_index_hashtree, riak_kv_vnode_status_mgr, riak_repl_stats
concept: filesystem-layout

# Reviewed against

3.4.0: 89d6958c2b0fd429cb4a501852d0b32ad412b7f9a049b09b636f27c35f40e25f
3.4.1: e2a93196589a0f28edd586965956c4b5e595a915db59b29165e89f7bb0059159
