# Description

Number of replication consumer workers for each sink queue. More workers can drain queues faster when source, destination and network capacity permit; `replrtq_sinkpeerlimit` caps concurrency against a single peer.

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_replrtq_snk
concept: concurrency, cross-cluster-replication

# Reviewed against

3.4.0: 128bad67c56cc0ff36092c2f48d7ffb9c61223dbf0a5c9fb844f0150dc1952b4
3.4.1: c3c412799410008ff484c4d030a7a6a68dc30e38e07390427c4e800d0f8e4de3
