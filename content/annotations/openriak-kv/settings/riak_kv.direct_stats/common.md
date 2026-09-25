# Description

Controls creation of the sidejob resource used for KV statistics updates. When true, startup skips the statistics worker resource for the direct-update mode; when false, it creates the bounded worker resource.

# Datatype

Boolean

# Allowed values

- `true`
- `false`

# Constraints

- Use the Erlang atoms `true` or `false`.

# Inferred default

`false`.

# Tags

feature: observability
repository: riak_kv
module: riak_kv_app
concept: concurrency, diagnostics

# Notes

This is the Erlang application environment key `direct_stats` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_app.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_app.erl#L67)

# Reviewed against

3.4.0: 24d81b432473716b7b9a53dbada24527e52f99c64aebd1456d786ec4334c98a2
3.4.1: 7240b7efa6b3aeba8674fa346553df9ffca4342b4bccacd1c22d1c399e8e35bc
