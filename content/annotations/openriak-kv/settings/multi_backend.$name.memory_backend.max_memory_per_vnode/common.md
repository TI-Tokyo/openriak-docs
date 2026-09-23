# Description

For the named backend `$name`: Memory allowance for each memory-backend vnode. Total backend memory scales with the number of vnodes on the node; this is not a whole-node memory budget and the data is not durable on disk. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: memory-backend
repository: riak_kv
module: riak_kv.schema
concept: memory, storage

# Reviewed against

3.4.0: a014813c4410760884c638eb090bf1017a7fe09fef5a66414a8034ffc1e8cdb2
3.4.1: 73da698d94d817abded4d4fbf65f92985469f85da6c61e02a099a7eedce2dc4a
