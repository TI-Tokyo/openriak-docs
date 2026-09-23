# Description

Maximum number of updates allowed while reusing a Bitcask fold snapshot. Used with `bitcask.fold.max_age` to decide whether a fold can reuse the key directory or must wait for a fresh snapshot. `unlimited` disables this update-count limit.

# Tags

feature: bitcask
repository: bitcask
module: bitcask.schema
concept: storage

# Reviewed against

3.4.0: 2185e198aa94ed2765b883b9d3d363b3a2c8f8490c24eb276aff99910f356926
3.4.1: 2185e198aa94ed2765b883b9d3d363b3a2c8f8490c24eb276aff99910f356926
