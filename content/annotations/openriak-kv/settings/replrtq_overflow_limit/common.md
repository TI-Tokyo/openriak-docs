# Description

Maximum overflow-queue size for each replication queue name and priority on this node. New additions beyond the limit are discarded. A runtime limit change takes effect on a newly created queue; clearing an existing queue also discards its pending work.

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_replrtq_src
concept: cross-cluster-replication, queueing

# Reviewed against

3.4.0: bb6331c671bb113a83760f1f034156977a195e0e189e05222cafe4be209127c2
3.4.1: 647166f75468ae39bde67c4619c583373533cd148502e4a4832aff2251806f52
