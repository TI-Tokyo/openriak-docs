# Description

Number of node-wide AF3 workers when `worker_pool_strategy = dscp`. AF3 handles AAE full-sync queries scoped to a bucket or key range. More workers can accelerate repair queries while increasing competition with foreground requests.

# Tags

feature: worker-pools
repository: riak_kv
module: riak_kv_app
concept: background-work, concurrency

# Reviewed against

3.4.0: 9f12cb8f38178acd739ee16b7064557157fa01d5f2e80ad6e4934a7251a2c8f7
3.4.1: 2a3ae1fa83202237b6e2d8092ef8e567c3cbb12382d272527b4070ae22b4a72f
