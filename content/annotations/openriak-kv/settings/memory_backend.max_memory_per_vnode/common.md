# Description

Memory allowance for each memory-backend vnode. Total backend memory scales with the number of vnodes on the node; this is not a whole-node memory budget and the data is not durable on disk.

# Tags

feature: memory-backend, storage-backends
repository: riak_kv
module: riak_kv.schema
concept: backend-selection, memory, storage

# Reviewed against

3.4.0: a855104c5e0f7ae9e11d78adcda629e41344a2b35c15ca020cd7198c2fe19130
3.4.1: a71d12afa043d9af916325d39e82ce134919d7a3cfba2ab23504ea66e057f5f5
