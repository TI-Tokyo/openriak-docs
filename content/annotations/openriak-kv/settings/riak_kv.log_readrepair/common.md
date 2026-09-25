# Description

Enables detailed logging of objects selected for read repair by Tictac AAE, including their bucket, key and compared vector clocks. Useful when investigating repeated replica differences.

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

feature: tictac-aae
repository: riak_kv
module: riak_kv_tictacaae_repairs
concept: diagnostics, replica-repair

# Notes

This is the Erlang application environment key `log_readrepair` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_tictacaae_repairs.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_tictacaae_repairs.erl#L201)

# Reviewed against

3.4.0: 904fd99deb1e3598e015c5b5111585d7c8c224d8186ce352b185e69385df7a7c
3.4.1: 4404b9726bcb170f67bd679ed51059bb84b1aea6d4e3c25d47ef1e93f6841826
