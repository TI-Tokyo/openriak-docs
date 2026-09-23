# Description

Default number of replica responses required for reads on untyped buckets. A larger requirement waits for more responses; `notfound_ok` and `pr` further constrain which responses can satisfy a read.

# Tags

feature: bucket-properties
repository: riak_kv
module: riak_kv.schema
concept: data-policy, quorums

# Reviewed against

3.4.0: 948878492a1f1654486107423f56f042e83f398242a89d1687efe43b72decbb5
3.4.1: d0c16b2fff97502f224d8c8dcea391ff9eed4764f4c54312441144c5fc0a6370
