# Description

Default number of pending inputs accumulated before invoking a MapReduce reduce function. Individual reduce phases can override the batch size or request a single final batch.

# Datatype

Integer

# Units

- items

# Constraints

- Expected to be a positive batch count. A query can override it; `reduce_phase_only_1` uses an internal atom sentinel to collect one whole phase.

# Inferred default

`20`.

# Tags

feature: query-processing
repository: riak_kv
module: riak_kv_w_reduce
concept: memory, querying

# Notes

This is the Erlang application environment key `mapred_reduce_phase_batch_size` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_w_reduce.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_w_reduce.erl#L270)

# Reviewed against

3.4.0: 2ffe08ebab1a1a16ec103c30722aca82fd8c1e072aa31927b397bc718ea411df
3.4.1: ae9caa5bd0b88e49de194a1cde82680b663c89b428b3fb21370b6da830721487
