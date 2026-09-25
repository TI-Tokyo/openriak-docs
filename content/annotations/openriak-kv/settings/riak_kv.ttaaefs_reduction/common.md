# Description

Fractional reduction threshold used to decide whether to repeat a range-tree comparison before fetching clocks. The override must be a float from `0.0` to `1.0`; higher thresholds require greater reduction to justify another comparison.

# Datatype

Floating-point number

# Constraints

- Validated as an Erlang float in the inclusive range `0.0..1.0`. Integer `0` or `1` is not accepted as an override.

# Inferred default

Unset; the AAE exchange retains its `0.3` worthwhile-reduction default.

# Tags

feature: full-sync
repository: riak_kv
module: riak_kv_ttaaefs_manager
concept: replica-repair, cross-cluster-replication

# Notes

This is the Erlang application environment key `ttaaefs_reduction` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_ttaaefs_manager.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_ttaaefs_manager.erl#L991)

Additional type/default evidence:

- [kv_index_tictactree/src/aae_exchange.erl](https://github.com/OpenRiak/kv_index_tictactree/blob/705309988ba9fc448350b7e782fd1bfe1ab3a8c3/src/aae_exchange.erl)

# Reviewed against

3.4.0: 945f69432d95332630d69b2b03b752eb1dd0482f03856deb86175aadb282df78
3.4.1: 945f69432d95332630d69b2b03b752eb1dd0482f03856deb86175aadb282df78
