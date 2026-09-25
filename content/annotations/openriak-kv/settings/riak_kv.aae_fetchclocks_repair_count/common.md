# Description

Internal counter used to create a new tree-repair identifier when fetch-clocks repair is enabled. The full-sync manager increments it so a newly requested repair can be distinguished from a repair already handled.

# Datatype

Integer

# Constraints

- Expected to be a non-negative integer. Non-integer values produce an effective repair count of `1`.

# Inferred default

`0`; the manager adds one, giving an initial repair count of `1`.

# Tags

feature: tictac-aae
repository: riak_kv
module: riak_kv_ttaaefs_manager
concept: replica-repair, runtime

# Notes

This is the Erlang application environment key `aae_fetchclocks_repair_count` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_ttaaefs_manager.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_ttaaefs_manager.erl#L1047)

# Reviewed against

3.4.0: 9ab6dfbf7f7ed40693d65f495737b00f361bcb25cf85b3b7cc8c655331c4c975
3.4.1: ad237fdd7baf515d2d8e910face3914f4021ee7eddd9e79161a9a565d5b84ecf
