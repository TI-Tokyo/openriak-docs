# Description

Internal snapshot of registered KV hooks. The hooks registry saves it in the application environment so it can restore its ETS table after a supervisor restart.

# Datatype

List

# Constraints

- List of `{conditional_postcommit, {Module, Function}}` entries. The callback is invoked with bucket type, bucket and properties (arity 3).

# Inferred default

Unset; no saved hooks are restored. Hook registration writes the current ETS contents to this key.

# Tags

feature: object-storage
repository: riak_kv
module: riak_kv_hooks
concept: runtime

# Notes

This is the Erlang application environment key `riak_kv_hooks` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_hooks.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_hooks.erl#L120)

# Reviewed against

3.4.0: 65eb23d60b90426f6c0c3582df63ee16376ea8c45a0aaca214f78e8b2bce75bf
3.4.1: 3376042dae44611f2ef3895ccdd0e36c7802cf6d35e872b339e9539d1a8b249f
