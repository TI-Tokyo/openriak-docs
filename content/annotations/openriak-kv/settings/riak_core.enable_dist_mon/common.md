# Description

Controls whether Riak Core starts its Erlang distribution monitor, which applies the configured send and receive buffer sizes to distribution sockets.

# Datatype

Boolean

# Allowed values

- `true`
- `false`

# Constraints

- Use the Erlang atoms `true` or `false`.

# Inferred default

`true`.

# Tags

feature: erlang-runtime
repository: riak_core
module: riak_core_sup
concept: connections

# Notes

This is the Erlang application environment key `enable_dist_mon` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_sup.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_sup.erl#L53)

# Reviewed against

3.4.0: c738bf24e0963645c31008a4d1ac9362858350d1cbec7e847c7b398c6170fa55
3.4.1: c738bf24e0963645c31008a4d1ac9362858350d1cbec7e847c7b398c6170fa55
