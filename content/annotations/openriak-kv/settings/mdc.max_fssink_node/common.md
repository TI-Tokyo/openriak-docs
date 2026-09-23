# Description

Hard limit on full-sync workers on each sink node, shared by all source clusters using that node. Raising source concurrency alone cannot exceed the receiving node's capacity limit.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl2_fs_node_reserver, riak_repl2_fscoordinator_serv, riak_repl_console
concept: cross-cluster-replication

# Reviewed against

3.4.0: e20dc047472ae8a9e99db06a52521e9f8995b382aadebc242f156beb1c34a301
3.4.1: e20dc047472ae8a9e99db06a52521e9f8995b382aadebc242f156beb1c34a301
