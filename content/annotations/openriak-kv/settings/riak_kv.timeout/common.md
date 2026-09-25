# Description

Application-wide GET state-machine timeout, in milliseconds, that takes precedence over the request's own timeout when set. When absent, the request option or built-in GET timeout is used.

# Datatype

Timeout

# Units

- milliseconds

# Constraints

- Non-negative integer timeout, or `infinity`. A configured application value takes precedence over the request option.

# Inferred default

Unset; use the request's `timeout` option, falling back to `60000`.

# Tags

feature: request-processing
repository: riak_kv
module: riak_kv_get_fsm
concept: quorums, runtime

# Notes

This is the Erlang application environment key `timeout` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_get_fsm.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_get_fsm.erl#L317)

# Reviewed against

3.4.0: 81c5284b2de9abdc53651a571b5ab4c20dc572d5beeb4f9c3d529f2d435a3cbe
3.4.1: 58d60c9f2ce8ba41922b8722fcb45de7ddbd412715ad94ff1bb85d70c3f2cbbd
