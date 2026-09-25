# Description

Staggers each vnode's initial exchange-work step using its partition hash. This helps prevent vnodes started together from refilling their AAE work queues in lockstep; tests can disable the staggering.

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

feature: tictac-aae
repository: riak_kv
module: riak_kv_vnode
concept: scheduling, replica-repair

# Notes

This is the Erlang application environment key `tictacaae_stepinitialtick` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_vnode.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_vnode.erl#L368)

# Reviewed against

3.4.0: 61c95b12f207e8491c4ddffe51ec30648a064c83508524e055c77fce6bfce5ba
3.4.1: e33f385734c014958a0647c0592fab6f43ec03e88062accd170e339ca3630bc7
