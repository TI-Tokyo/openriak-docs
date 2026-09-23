# Description

Choose where background query work is queued: `none` uses vnode pools, `single` uses one node-wide pool, and `dscp` separates work into service-class pools. Configure the corresponding pool sizes; these pools are distinct from Erlang schedulers.

# Tags

feature: worker-pools
repository: riak_kv
module: riak_kv_app, riak_kv_vnode
concept: background-work, concurrency

# Reviewed against

3.4.0: 1c38e9799008f09b70bf39700d9a7dc6a79cc01da9b331fe46fc0d83b2dc8d72
3.4.1: 2e4005cd0e5eeb8be1d16f4cff59db908b1bd72aa2fca53c9501c080166dd7e4
