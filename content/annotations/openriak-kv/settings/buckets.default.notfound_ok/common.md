# Description

Decide whether a replica's not-found response counts toward a read quorum for untyped buckets. When disabled, `basic_quorum` can still let a majority of missing responses end a read early.

# Tags

feature: bucket-properties
repository: riak_kv
module: riak_kv.schema
concept: data-policy

# Reviewed against

3.4.0: 8ac4c4f66528dd99d8810cbeec4ae38386b8b4f66db936751fc5f01310e57990
3.4.1: 981a8ec9b266b15fdd4d5eb84244c9910565921e5ab3d91c7b33fb712f64ead0
