# Description

Active-GET count above which read repair is increasingly likely to be skipped as load approaches `riak_kv.read_repair_max`. Below this threshold repairs proceed normally; if unset it falls back to the hard limit.

# Datatype

Integer or atom

# Units

- active GETs

# Constraints

- Non-negative integer soft limit, normally no greater than the hard limit. `undefined` uses the hard limit.

# Inferred default

The value of `riak_kv.read_repair_max`; unset if the hard limit is unset.

# Tags

feature: read-repair
repository: riak_kv
module: riak_kv_get_fsm
concept: overload-protection, replica-repair

# Notes

This is the Erlang application environment key `read_repair_soft` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_get_fsm.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_get_fsm.erl#L666)

# Reviewed against

3.4.0: fdd3ae1273014a7d0f89a98e647ef87887132238214c1232d6bb9c7817b29150
3.4.1: cc4841e33684ea86855d65414cb2b4fa229c931c487372ec82a13493cda45d50
