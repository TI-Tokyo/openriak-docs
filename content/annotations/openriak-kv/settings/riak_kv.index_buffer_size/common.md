# Description

Number of secondary-index results buffered by a vnode before sending a batch. It controls result-message granularity and memory use during index folds.

# Datatype

Integer

# Units

- results

# Constraints

- Expected to be a positive integer.

# Inferred default

`100`.

# Tags

feature: secondary-indexes
repository: riak_kv
module: riak_kv_vnode
concept: memory, querying

# Notes

This is the Erlang application environment key `index_buffer_size` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_vnode.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_vnode.erl#L991)

# Reviewed against

3.4.0: b251fe17071c15ae6b8d233638a5a3dba41f9efc8588f8944d396f7f38bfc41a
3.4.1: f336e54c73b80ff9eb49b5d40530a1384db0d8fa8bf8c3468d6c22b2e424a688
