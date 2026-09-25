# Description

Modules that handle cluster broadcast messages and anti-entropy exchanges. Each must implement the `riak_core_broadcast_handler` behaviour; the default handler is the cluster metadata manager.

# Datatype

List

# Constraints

- List of module atoms implementing `riak_core_broadcast_handler`.

# Inferred default

`[riak_core_metadata_manager]`.

# Tags

feature: cluster-management
repository: riak_core
module: riak_core_broadcast
concept: replica-repair

# Notes

This is the Erlang application environment key `broadcast_mods` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_broadcast.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_broadcast.erl#L119)

# Reviewed against

3.4.0: 4c37cee377f1d1c6ea3460aed3b2acea2d53ee96b0d54dc175dee242ea5d2c17
3.4.1: 4c37cee377f1d1c6ea3460aed3b2acea2d53ee96b0d54dc175dee242ea5d2c17
