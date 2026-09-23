# Description

For the named backend `$name`: Maximum expected lifetime, in seconds, of a Leveled index-query snapshot. Queries exceeding it risk losing the snapshot; increase only when long queries and retained-file costs are understood. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveled
repository: leveled
module: leveled_multi.schema
concept: scheduling, storage

# Reviewed against

3.4.0: 78bb7ee054fb00aeddcd4e91efbc44ed73bc065ef21f6faa869f9daed066ee46
3.4.1: 158ee2887cf0651bad2fe2b39b9e4109bd69a0253eb39b983f54b0763ececb58
