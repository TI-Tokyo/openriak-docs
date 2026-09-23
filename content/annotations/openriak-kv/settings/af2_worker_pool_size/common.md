# Description

Number of node-wide AF2 workers when `worker_pool_strategy = dscp`. AF2 handles coverage work that the backend queues, including supported key-listing and secondary-index folds. More workers can reduce queueing but increase backend load.

# Tags

feature: worker-pools
repository: riak_kv
module: riak_kv_app
concept: background-work, concurrency

# Reviewed against

3.4.0: d77dfddee053be966be7babb18912f19950e224177701f8bcea08a011a13b590
3.4.1: 02c43e495f7756be633675a512c169f27f32f54e5c0b3f3b2ba1981e47a0c19f
