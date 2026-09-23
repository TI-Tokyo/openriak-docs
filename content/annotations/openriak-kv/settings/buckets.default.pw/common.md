# Description

Default minimum number of primary replicas required to acknowledge writes on untyped buckets. Fallback acknowledgements do not count toward this condition; it is additional to `w` and `dw`.

# Tags

feature: bucket-properties
repository: riak_kv
module: riak_kv.schema
concept: data-policy, quorums

# Reviewed against

3.4.0: 7b38b1f7066bdc1cbbb382a6c3c290e8441e90d62e26108aa60486ed12634f0a
3.4.1: fc39db5de9e0c9522b9b86acb00553332a4b07f7dcd286d6f573bad94608ea52
