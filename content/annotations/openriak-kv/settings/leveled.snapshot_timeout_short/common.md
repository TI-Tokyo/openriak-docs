# Description

Maximum expected lifetime, in seconds, of a Leveled index-query snapshot. Queries exceeding it risk losing the snapshot; increase only when long queries and retained-file costs are understood.

# Tags

feature: leveled
repository: leveled
module: leveled.schema
concept: scheduling, storage

# Reviewed against

3.4.0: e4b090601da841dca2b0f03c65c96fa9ca611f5c58b3c768149935af5f761444
3.4.1: d43771470b4cb2a777f34360239d6bf3af92bb4ebc237758810325dc3a0421e5
