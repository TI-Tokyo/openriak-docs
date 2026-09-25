# Description

Compression applied when serializing Riak data types. Integer levels run from 0 to 9; `off` corresponds to 0 and `on` to 6. Higher levels can save space at greater CPU cost.

# Constraints

- Integer compression levels must be from 0 through 9 inclusive. The flag values `on` and `off` are also accepted; they select levels 6 and 0 respectively.

# Notes

Checked against the [compression schema and validator](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/priv/riak_kv.schema#L966). Cuttlefish converts `on` and `off` to booleans before the validator tests them. The same checks apply in 3.4.0 and 3.4.1.

# Tags

feature: data-types
repository: riak_kv
module: riak_dt
concept: compression, data-model

# Reviewed against

3.4.0: 80990cbe21863a176d97cc80fc242af04fd573714d2aff0a3f391448aae80462
3.4.1: d333bec6b8e9d4580431d98289ea1028c51e37335f27f4801ba15500338ea106
