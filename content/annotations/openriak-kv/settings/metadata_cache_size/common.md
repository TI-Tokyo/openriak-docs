# Description

Per-vnode metadata-cache size, or `off` to disable it. The accounting measures the ETS table rather than all associated data, so actual memory can exceed the limit multiplied by vnode count. Benchmark before enabling it for a workload.

# Tags

feature: object-storage
repository: riak_kv
module: riak_kv_vnode
concept: data-model, memory

# Reviewed against

3.4.0: bac0f12d858fa6d43bd6a75b1af2e929d56f829b494fc6d2e7ac416afd08f404
3.4.1: 69df5ce0e1261adf88d7e3447dfc734487b4588c674dc8ef52e3042573249225
