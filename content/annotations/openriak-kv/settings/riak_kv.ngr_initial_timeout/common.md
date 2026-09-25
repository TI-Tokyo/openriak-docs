# Description

Startup wait, in milliseconds, used by next-generation replication services to let KV become ready and stable before beginning work. The source describes changing it primarily for tests.

# Datatype

Integer

# Units

- milliseconds

# Constraints

- Positive integer according to the consumer type specification.

# Inferred default

`60000`.

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_util
concept: scheduling, cross-cluster-replication

# Notes

This is the Erlang application environment key `ngr_initial_timeout` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_util.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_util.erl#L290)

# Reviewed against

3.4.0: 104f231c80bf89c22ea1f1a831630db1d8803e711794a177457bc561c077cea0
3.4.1: 182446fa294b2aaae4a580ce7bee0e35463597b0afea52d4ba0c0d810a22e437
