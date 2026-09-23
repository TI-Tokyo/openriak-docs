# Description

Compression applied when serializing Riak data types. Integer levels run from 0 to 9; `off` corresponds to 0 and `on` to 6. Higher levels can save space at greater CPU cost.

# Tags

feature: data-types
repository: riak_kv
module: riak_dt
concept: compression, data-model

# Reviewed against

3.4.0: 6d9e3cb5832cba68542e5f98b433663b047bcd44ef27fd532e4ec9ddbbf87d13
3.4.1: d675009a6289526eb871d66d1fca0764cde66a0b1297b5bc834400a1fcaeb774
