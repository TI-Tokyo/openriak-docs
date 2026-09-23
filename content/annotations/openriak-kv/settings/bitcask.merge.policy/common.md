# Description

Choose when Bitcask merges may start: `always`, `never`, or `window`. Window mode uses `bitcask.merge.window.start` and `.end`; disabling merges allows obsolete data files to accumulate.

# Tags

feature: bitcask
repository: bitcask
module: bitcask_merge_worker
concept: compaction, storage

# Reviewed against

3.4.0: df1e1fb6764a599c96ea4b516555e604e22d7cd1a9c262e8cb3074f6e052549b
3.4.1: df1e1fb6764a599c96ea4b516555e604e22d7cd1a9c262e8cb3074f6e052549b
