# Description

Space-separated Erlang hooks to run after an object is stored in an untyped bucket. Use `module:function` entries. Unlike precommit hooks, these run after the write and cannot reject it beforehand.

# Tags

feature: bucket-properties
repository: riak_kv
module: riak_kv.schema
concept: data-policy

# Reviewed against

3.4.0: 81a7297cc08f34e257c74135e0e7420ff74e8aa13d3afba8a50b6af30240908f
3.4.1: 309b0f343e48237f68d2ef8d9e263c1d934a5c968f2048655953f4383c6cef31
