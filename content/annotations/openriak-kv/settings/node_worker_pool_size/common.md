# Description

Number of workers in the shared node-wide pool when `worker_pool_strategy = single`. The `dscp` strategy instead uses `af1_worker_pool_size` through `af4_worker_pool_size` and `be_worker_pool_size`; `none` uses vnode pools.

# Tags

feature: worker-pools
repository: riak_kv
module: riak_kv_app
concept: background-work, concurrency

# Reviewed against

3.4.0: 78dff78fb0e8c368f63f9bb6cbd39e9abcd416f1c4dd4a07c4c14b1e99f4a9d0
3.4.1: 0eaa42865b1ee270cf47cd8437d7df48b0a46a08bbf10dc10ec09c5340a18b43
