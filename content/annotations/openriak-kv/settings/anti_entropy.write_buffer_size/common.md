# Description

Size of the LevelDB write buffer used for legacy AAE hash-tree storage. It affects AAE memory and flush behaviour, independently of write buffers in the user-data backend.

# Tags

feature: legacy-aae
repository: riak_kv
module: riak_kv.schema
concept: memory, replica-repair

# Reviewed against

3.4.0: 0dd36c3d37e613f7ccc3e9c0cbb86d7da61cc02038379477ccce2b4d93c0a838
3.4.1: a334d8c7c2e2e5e2e643b1eccced4c48795066e55c3668a31e10de4ec244c486
