# Description

Maximum reaper overflow-queue size. Excess additions are discarded. Applying a new limit at runtime requires starting a fresh queue, for example with `riak_kv_reaper:clear_queue()`, which also clears pending work.

# Tags

feature: deletion
repository: riak_kv
module: riak_kv_reaper
concept: queueing, tombstones

# Reviewed against

3.4.0: 0deca927e393f500779b36c3d8bc00c74fac433ff9ff26b044194b7568d4d0fc
3.4.1: a1778e40fbd25e9a5d5f90e57904a90be21920d29ce7186aa2ae1811145a9a6c
