# Description

Default source queue name consumed by this sink node. Peers without an explicit queue use this name; multiple peers can serve it. Additional runtime queues can be added through the sink API but are separate from this default.

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_replrtq_peer, riak_kv_replrtq_snk
concept: cross-cluster-replication, queueing

# Reviewed against

3.4.0: 4973c8d829b3c409c2355c75ca504e793e6a52f7fd1bcdd232a90c790438d31a
3.4.1: 952d9b628c7faf87105081992e73c2c9f277c59a53f69a342f68c39a4ede3ded
