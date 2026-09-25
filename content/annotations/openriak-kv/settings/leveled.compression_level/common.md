# Description

Ledger LSM-tree level from which Leveled applies compression. This is a tree-level threshold, not a codec's compression-strength setting.

# Constraints

- Use an integer from 0 through 7 inclusive to select the first LSM-tree level to compress.

# Tags

feature: leveled
repository: leveled
module: leveled.schema
concept: compression, storage

# Reviewed against

3.4.0: 611f54022157604c855b7b6d83f59c07608c0a311a1813240d8b688dc7a6d538
3.4.1: b4e094b48a246f71591a8425d049aecf35408f48d0a195a4bae74b81a4602bce
