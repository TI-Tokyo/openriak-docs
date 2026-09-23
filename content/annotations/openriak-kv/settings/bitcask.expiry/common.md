# Description

Age after which Bitcask objects expire. Use a duration such as `1d`, or `off` to retain objects without age-based expiry. This is backend retention, separate from Riak's tombstone deletion policy.

# Tags

feature: bitcask
repository: bitcask
module: bitcask.schema
concept: retention, storage

# Reviewed against

3.4.0: cad34961506b601f6389179bf8ed6ef9f5bfd3b7d269bfc695757e1b08fadfcf
3.4.1: cad34961506b601f6389179bf8ed6ef9f5bfd3b7d269bfc695757e1b08fadfcf
