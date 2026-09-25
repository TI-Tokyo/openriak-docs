# Description

Number of keys buffered by a vnode before sending a key-listing batch. Smaller values deliver results in more frequent messages; larger values increase the per-fold buffer.

# Datatype

Integer

# Units

- keys

# Constraints

- Expected to be a positive integer.

# Inferred default

`100`.

# Tags

feature: query-processing
repository: riak_kv
module: riak_kv_vnode
concept: memory, querying

# Notes

This is the Erlang application environment key `key_buffer_size` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_vnode.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_vnode.erl#L992)

# Reviewed against

3.4.0: 58bbf113cfa915645732acab8c11475f8c35ecbbebe3ae976f7a9d36b30a478b
3.4.1: 5cc0dc61327e975c4015c971559a38df23d9cc5252b9197c44bafe83b7e3a9d7
