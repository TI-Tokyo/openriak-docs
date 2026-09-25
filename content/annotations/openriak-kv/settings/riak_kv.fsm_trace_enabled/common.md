# Description

Enables the tracing hooks in GET and PUT request state machines, including bucket/key trace tags. These hooks are intended for request-path diagnostics with the supported tracing infrastructure.

# Datatype

Boolean

# Allowed values

- `true`
- `false`

# Constraints

- Use the Erlang atoms `true` or `false`.

# Inferred default

Unset (`undefined`); tracing is enabled only by `true`.

# Tags

feature: observability
repository: riak_kv
module: riak_kv_get_fsm, riak_kv_put_fsm
concept: diagnostics

# Notes

This is the Erlang application environment key `fsm_trace_enabled` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_get_fsm.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_get_fsm.erl#L188)
- [riak_kv/src/riak_kv_put_fsm.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_put_fsm.erl#L268)

# Reviewed against

3.4.0: ac0cb9a67a060195c4186285f864e72bbf9a8c6e4595d4ecaaea675c60c05063
3.4.1: b9c70ad05540a08777bc3d9e70351c0043fe7549eafd5e083af3414e3ee64a0b
