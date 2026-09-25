# Description

Additional path prefix for the legacy raw HTTP object API. The standard `riak` prefix remains registered when a custom prefix is supplied.

# Datatype

String

# Constraints

- Erlang character list naming an additional legacy HTTP route prefix.

# Inferred default

Unset; only the standard `"riak"` legacy route is added.

# Tags

feature: client-networking
repository: riak_kv
module: riak_kv_web
concept: compatibility

# Notes

This is the Erlang application environment key `raw_name` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_web.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_web.erl#L50)

# Reviewed against

3.4.0: 1d73daa454f66a99f3b4d0959a0b823558f1c6f08ee7ef258b0d3b40122cec42
3.4.1: eacf6334ee29df91f4846b9d4304d8b7406be2a322425c45e65f6db3e8568c58
