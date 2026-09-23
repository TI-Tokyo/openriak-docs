# Description

Number of node-wide AF1 workers when `worker_pool_strategy = dscp`. AF1 handles hot backups and rebuilding cached AAE trees. It is separate from the per-vnode pool and unused by the `single` or `none` strategies.

# Tags

feature: worker-pools
repository: riak_kv
module: riak_kv_app
concept: background-work, concurrency

# Reviewed against

3.4.0: b7ee10a3e3a48b0ea008187902f431fbf37ba23362022857bc1abaf952f9d579
3.4.1: 49e4e38dc4ee26093cc481f673de283eff4bca521afbaa0c7b168d605601c2ef
