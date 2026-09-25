# Description

Temporarily suspends Tictac exchange participation: incoming AAE requests return `not_supported`, and scheduled exchange pokes skip work. It does not disable ordinary object storage or remove the AAE store.

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
module: riak_kv_vnode
concept: replica-repair

# Notes

This is the Erlang application environment key `tictacaae_suspend` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_vnode.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_vnode.erl#L1123)

# Reviewed against

3.4.0: 4ed891f7d11ecdf3c81d8ad76cd1524345fe9537c255e4a8d39f7f52b3ff10a1
3.4.1: e3ac3828e1644400f00cb4af6c72c84ed0e9bacb29eb73b055bb143257d8e8c5
