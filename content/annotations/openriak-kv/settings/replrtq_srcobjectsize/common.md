# Description

Largest object eligible for inline caching in a replication queue. Larger objects still replicate but must be fetched again. Together with `replrtq_srcobjectlimit`, this bounds cached object payload memory.

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_vnode
concept: cross-cluster-replication

# Reviewed against

3.4.0: 6871c163c873ae6c225ca87bfe0da0c052e122354cb0b2e3f9907f756e5f1e05
3.4.1: 8404841fd4cbe75381f3ddd79b59c9c5ca61aa5989d85985927eb099ffd28e8e
