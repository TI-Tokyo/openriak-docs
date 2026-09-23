# Description

Allow this node to replicate tombstone-reap requests to other clusters. Reaping removes deletion markers, so coordinate it with the retention and reconciliation policy of connected clusters.

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_reaper
concept: cross-cluster-replication

# Reviewed against

3.4.0: 3fd7afeff41d705e05a84c56e1eac11596ded6a13858571590e2785ebcb320c3
3.4.1: 1afc1745f9d1f2a6f7ef485621636e1361885c6b59f0387a48149334012234fd
