# Description

Minimum scheduled delay, in seconds, for replication peer discovery. It also supplies the initial discovery delay; subsequent delays are randomized between the configured minimum and maximum.

# Datatype

Integer

# Units

- seconds

# Constraints

- Expected to be a positive integer.

# Inferred default

`60`.

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_replrtq_peer
concept: scheduling, cross-cluster-replication

# Notes

This is the Erlang application environment key `replrtq_prompt_min_seconds` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_replrtq_peer.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_replrtq_peer.erl#L128)

# Reviewed against

3.4.0: 8fdad8b80e073ad7ad2da15661b2d7039a24f85ef7f862608a0167fbf344eae1
3.4.1: f36aba84da993a01d27c6553a6a40e8a808f04cf86b26e83a3581785c4982814
