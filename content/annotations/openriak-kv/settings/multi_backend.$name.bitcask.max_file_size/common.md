# Description

For the named backend `$name`: Size threshold for rolling a Bitcask data file. A write that takes the current file beyond the threshold causes subsequent writes to use a new file; the threshold is not a total database-size limit. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: bitcask
repository: bitcask
module: bitcask_multi.schema
concept: storage

# Reviewed against

3.4.0: 024907ad83a000f418d6191e8d537b7da35ef246d16c0f0031c35fa1431aa5fd
3.4.1: 024907ad83a000f418d6191e8d537b7da35ef246d16c0f0031c35fa1431aa5fd
