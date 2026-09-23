# Description

For the named backend `$name`: Choose when Bitcask merges may start: `always`, `never`, or `window`. Window mode uses `bitcask.merge.window.start` and `.end`; disabling merges allows obsolete data files to accumulate. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: bitcask
repository: bitcask
module: bitcask_multi.schema
concept: compaction, storage

# Reviewed against

3.4.0: c92a7c33dcc9507cc301d5df4228297a81cfd758db147a0dd8069a279f3efe55
3.4.1: c92a7c33dcc9507cc301d5df4228297a81cfd758db147a0dd8069a279f3efe55
