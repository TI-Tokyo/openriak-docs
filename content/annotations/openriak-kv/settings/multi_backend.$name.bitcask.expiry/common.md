# Description

For the named backend `$name`: Age after which Bitcask objects expire. Use a duration such as `1d`, or `off` to retain objects without age-based expiry. This is backend retention, separate from Riak's tombstone deletion policy. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: bitcask
repository: bitcask
module: bitcask_multi.schema
concept: retention, storage

# Reviewed against

3.4.0: 28543a823b830cad89d2c32a318ba7969d4de3420600eb734ea431aba955b179
3.4.1: 28543a823b830cad89d2c32a318ba7969d4de3420600eb734ea431aba955b179
