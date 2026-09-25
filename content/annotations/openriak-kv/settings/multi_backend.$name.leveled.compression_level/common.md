# Description

For the named backend `$name`: Ledger LSM-tree level from which Leveled applies compression. This is a tree-level threshold, not a codec's compression-strength setting. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Constraints

- Use an integer from 0 through 7 inclusive to select the first LSM-tree level to compress.

# Tags

feature: leveled
repository: leveled
module: leveled_multi.schema
concept: compression, storage

# Reviewed against

3.4.0: 99ec2850c07e2ea80aae4e63e03a01d0853ef90bd41f4d2ccc4fc2a1fe6f5850
3.4.1: 3b19b2bc3241edfd975d06341f11d4f2e375162fa9ae7968dd80f23914716d12
