# Description

Compress objects with zlib during queue-based replication transfer. This can reduce network traffic for compressible values at the cost of compression and decompression CPU work.

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_pb_object, riak_kv_wm_queue
concept: compression, cross-cluster-replication

# Reviewed against

3.4.0: 9fbd41167617f3528314c0bc7631c4e90e648c459ac6cc364860d31983e5bfbb
3.4.1: 2318f251137662f04a40586454f716b90cc03155d1d48a84b1c3bacf5d79a0c0
