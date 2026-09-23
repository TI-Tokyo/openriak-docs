# Description

Random variation added to Bitcask merge-check scheduling. Jitter spreads checks across partitions so they are less likely to compete for disk resources at the same time.

# Tags

feature: bitcask
repository: riak_kv
module: riak_kv_bitcask_backend
concept: compaction, storage

# Reviewed against

3.4.0: dbd2635970a6efd20383717050ffeec882f35a0a34a54c46a8d1e85c41f1b16f
3.4.1: a94db9933ab803698d50a1ab0e395e73733ed9dbb4533e20f224c1442b10a1f0
