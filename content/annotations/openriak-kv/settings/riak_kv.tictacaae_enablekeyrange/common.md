# Description

Allows prompted Tictac repair exchanges to restrict subsequent work to the key range inferred from detected differences. The optimization also requires the cluster's prompted-repair capability.

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
concept: replica-repair

# Notes

This is the Erlang application environment key `tictacaae_enablekeyrange` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_tictacaae_repairs.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_tictacaae_repairs.erl#L299)

# Reviewed against

3.4.0: 3358259d94b565254e3a509ac42ce4f8c9cc6982e3bedf731b715da820fae803
3.4.1: 154cd6c5001f3f256eefa2f2246bd4a62551b3910634f36c5e06cef88c815b1c
