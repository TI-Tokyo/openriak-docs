# Description

Number of node-wide best-effort workers when `worker_pool_strategy = dscp`. This pool handles rebuilding parallel AAE stores and is separate from the cached-tree rebuild work assigned to AF1. It is unused by the `single` and `none` strategies.

# Tags

feature: worker-pools
repository: riak_kv
module: riak_kv_app
concept: background-work, concurrency

# Reviewed against

3.4.0: c8397d68274ba2b4d5db190d37624f19a7cef5199876da40790242af232984bd
3.4.1: dfb5d552c69cab149d8b1ecfe1c427fe825d0b09c65baa8ee9843111ceae562c
