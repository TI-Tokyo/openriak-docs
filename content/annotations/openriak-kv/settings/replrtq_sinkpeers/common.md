# Description

Source-peer list for queue-based replication, with entries in `host:port:protocol` form. Every source node's queue needs consumers. An optional `queuename:` prefix is supported, but a single queue name per sink node is the recommended arrangement.

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_replrtq_peer, riak_kv_replrtq_snk
concept: cross-cluster-replication

# Reviewed against

3.4.0: 8748d6dcf6b3b959e10c1f81bda73a9d6e4ac69c19fdee40f3f7c584b701a1f6
3.4.1: ba7d211a49d98902629637fe49401a8677b1ab3b3fd4aaaa9b10387c340c7415
