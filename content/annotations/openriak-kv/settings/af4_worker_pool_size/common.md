# Description

Number of node-wide AF4 workers when `worker_pool_strategy = dscp`. AF4 handles operational AAE queries such as object statistics, replication-transition folds and reaping work. Other service classes retain their own concurrency limits.

# Tags

feature: worker-pools
repository: riak_kv
module: riak_kv_app
concept: background-work, concurrency

# Reviewed against

3.4.0: c4a59e41ec9b7d51ce361f8a38b7de84e090311eebb27903564d41b7142bdb0e
3.4.1: 19daf0329e0cdfebb6fc64ff7dca98f59f37c317205bf05eab4a38b54168a1ed
