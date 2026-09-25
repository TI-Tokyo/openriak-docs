# Description

HTTP path component used for the MapReduce endpoint. The source fallback is `mapred`, producing the `/mapred` route.

# Datatype

String

# Constraints

- Erlang character list used as the HTTP route prefix.

# Inferred default

`"mapred"`.

# Tags

feature: query-processing
repository: riak_kv
module: riak_kv_web
concept: querying

# Notes

This is the Erlang application environment key `mapred_name` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_web.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_web.erl#L194)

# Reviewed against

3.4.0: 361b43b1cf445ff134d9e5eca7cd3a83cd9b66e4c8ca252bc59be028c2a91bb3
3.4.1: ea4fdf518ce20245d64ffb5aba9a5e95578561a00d01f8d95d3dec0e3f2a0b55
