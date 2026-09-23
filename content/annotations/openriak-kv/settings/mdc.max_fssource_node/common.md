# Description

Hard limit on full-sync source workers on an individual node, shared across enabled full-sync destinations. It bounds node-level pressure even when several destination clusters are syncing.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl2_fscoordinator, riak_repl_console
concept: cross-cluster-replication

# Reviewed against

3.4.0: 0334e160a04d3e0d20fc082c40300baa9e9e0f998ae69ae052b320487be7dcf1
3.4.1: 0334e160a04d3e0d20fc082c40300baa9e9e0f998ae69ae052b320487be7dcf1
