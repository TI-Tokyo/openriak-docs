# Description

Resolve conflicting object versions by timestamp in untyped buckets. This can discard concurrent updates; use it only when that conflict policy matches the application's data model.

# Tags

feature: bucket-properties
repository: riak_kv
module: riak_kv.schema
concept: data-policy

# Reviewed against

3.4.0: 59d084fecc2c5e9abde3d91a0310edfa48961c199f154b7799ff0e8064f42c6b
3.4.1: c03b9aaff53694cab17c1d86b43ffe5e08e870525ef9cfa2121a9d88cdf64e42
