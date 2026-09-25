# Description

Internal countdown of upcoming automatic Tictac full-sync checks to skip. The manager decrements it each time a scheduled auto-check is suppressed.

# Datatype

Integer

# Units

- checks

# Constraints

- Expected to be a non-negative integer; a positive value is decremented on each suppressed check.

# Inferred default

`0`; the manager updates this counter as checks are suppressed.

# Tags

feature: full-sync
repository: riak_kv
module: riak_kv_ttaaefs_manager
concept: scheduling, runtime

# Notes

This is the Erlang application environment key `ttaaefs_autocheck_dropnext` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_ttaaefs_manager.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_ttaaefs_manager.erl#L1020)

# Reviewed against

3.4.0: 35d90ec575250803977c92f0ca90b0f6c0de83d941a24e22a19dad0ca423be6a
3.4.1: bc1143686bfd9fcec6a31adda5f1f3bc3f4fe15a3914bf268942762c0833fb0e
