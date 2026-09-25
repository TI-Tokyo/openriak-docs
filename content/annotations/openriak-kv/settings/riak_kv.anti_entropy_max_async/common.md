# Description

Number of asynchronous legacy hash-tree updates a vnode can issue before using a synchronous update to apply backpressure. This limits how far tree maintenance can lag behind vnode writes.

# Datatype

Integer

# Units

- updates

# Constraints

- Positive integer according to the consumer type specification.

# Inferred default

`90`.

# Tags

feature: legacy-aae
repository: riak_kv
module: riak_kv_vnode
concept: queueing, replica-repair

# Notes

This is the Erlang application environment key `anti_entropy_max_async` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_vnode.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_vnode.erl#L4310)

# Reviewed against

3.4.0: ddd18dcb74ac7e50d964a22e8e9f3768afd830e8a910bd563ea463f469e622e2
3.4.1: 6965bbfa6e2cde09fee5a883fb58930190d24836678d75fbbbd2ad963ffabadd
