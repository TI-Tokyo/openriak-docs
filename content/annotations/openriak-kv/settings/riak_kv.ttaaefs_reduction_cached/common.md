# Description

Nonnegative integer threshold passed to the exchange engine when deciding whether to repeat cached root or branch comparisons. It is a count threshold, unlike the fractional `riak_kv.ttaaefs_reduction` setting for range trees.

# Datatype

Integer

# Constraints

- Validated as an integer greater than or equal to zero.

# Inferred default

Unset; the AAE exchange retains its cached-reduction default of `0`.

# Tags

feature: full-sync
repository: riak_kv
module: riak_kv_ttaaefs_manager
concept: replica-repair, cross-cluster-replication

# Notes

This is the Erlang application environment key `ttaaefs_reduction_cached` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_ttaaefs_manager.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_ttaaefs_manager.erl#L998)

Additional type/default evidence:

- [kv_index_tictactree/src/aae_exchange.erl](https://github.com/OpenRiak/kv_index_tictactree/blob/705309988ba9fc448350b7e782fd1bfe1ab3a8c3/src/aae_exchange.erl)

# Reviewed against

3.4.0: 3e68291244acfb60143d004d52288a466edb51992b1122d4a029af59a01350c9
3.4.1: 3e68291244acfb60143d004d52288a466edb51992b1122d4a029af59a01350c9
