# Description

Optional delay, in milliseconds, inserted at the beginning of Riak Core application startup. When absent, startup proceeds immediately.

# Datatype

Integer

# Units

- milliseconds

# Constraints

- Expected to be a non-negative integer delay.

# Inferred default

Unset; startup inserts no delay.

# Tags

feature: cluster-management
repository: riak_core
module: riak_core_app
concept: runtime, scheduling

# Notes

This is the Erlang application environment key `delayed_start` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_app.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_app.erl#L41)

# Reviewed against

3.4.0: cc93fb244d73edcbf961fcb4d7c4e11ee03732e60a3d39ff32ba68f2851a2a71
3.4.1: cc93fb244d73edcbf961fcb4d7c4e11ee03732e60a3d39ff32ba68f2851a2a71
