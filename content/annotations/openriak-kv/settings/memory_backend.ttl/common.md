# Description

Lifetime assigned to values written to the memory backend. Once expired, an object is removed on the next read of its key; this differs from a background disk-retention policy.

# Tags

feature: memory-backend
repository: riak_kv
module: riak_kv.schema
concept: memory, retention, storage

# Reviewed against

3.4.0: ae7ba3b99bb7a28a555c7e8310c3a759742bdb75cf4e2281f5aa8a33404efed0
3.4.1: a78afd8599575608860f30ed03676adf5241d623461b9a0f8f969a74200ad7dc
