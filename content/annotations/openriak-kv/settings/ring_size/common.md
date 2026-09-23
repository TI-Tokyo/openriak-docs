# Description

Partition count used when initially creating a cluster. It must be a supported power of two. More partitions change distribution granularity and per-vnode overhead; editing this setting on an existing cluster is not a ring-resize operation.

# Tags

feature: cluster-management
repository: riak_core
module: riak_core, riak_core_ring, riak_core_vnode_manager, riak_kv_stat_bc
concept: partition-placement

# Reviewed against

3.4.0: 7acf17dac6bac6d9bfd409e1407c3321c8f56c137e4bcef293cdc393114c3665
3.4.1: a276624ad14e2a14e545bf0d81ac497f076c3c4bbb7e6d7c43db20be36cd036a

# Constraints

- Must be a power of 2.
- 2048 and larger are supported, but considered advanced config.
- Must be at least 8.
