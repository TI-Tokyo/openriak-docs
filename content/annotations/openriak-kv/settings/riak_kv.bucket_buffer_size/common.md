# Description

Number of bucket-listing results buffered by a vnode before sending a batch to the requesting process. Larger batches reduce message overhead but use more memory per fold.

# Datatype

Integer

# Units

- buckets

# Constraints

- Expected to be a positive integer buffer size.

# Inferred default

`1000`.

# Tags

feature: query-processing
repository: riak_kv
module: riak_kv_vnode
concept: memory, querying

# Notes

This is the Erlang application environment key `bucket_buffer_size` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_vnode.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_vnode.erl#L990)

# Reviewed against

3.4.0: 7af0911c74488387e929420c8711f37f637405e7a6e285171845cb882bfb48cd
3.4.1: b29455f58155e16ea6d492e580b4a6b7ba9075550297e14fe6872a102ab2c359
