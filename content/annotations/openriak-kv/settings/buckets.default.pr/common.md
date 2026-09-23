# Description

Default minimum number of primary replicas required to answer reads on untyped buckets. Fallback replicas do not satisfy this requirement, so raising it reduces read availability during failures.

# Tags

feature: bucket-properties
repository: riak_kv
module: riak_kv.schema
concept: data-policy, quorums

# Reviewed against

3.4.0: a18aff153c75b05ce3605eac5419fd5a6a293fc146271fe098a0734d3e27b64c
3.4.1: e22f09488af2aaeec3503b90620ea15b64741f1b6d4282f8bf1f2b2ef1cb18b8
