# Description

Lifetime, in milliseconds, of the cached statistics response used by the HTTP statistics endpoint. Repeated requests within this interval reuse the collected statistics.

# Datatype

Integer

# Units

- milliseconds

# Constraints

- Expected to be a non-negative integer.

# Inferred default

`1000`.

# Tags

feature: observability
repository: riak_kv
module: riak_kv_http_cache
concept: diagnostics

# Notes

This is the Erlang application environment key `http_stats_cache_milliseconds` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_http_cache.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_http_cache.erl#L52)

# Reviewed against

3.4.0: a5075f42657ff43d4cd969337495ecdf8403b22223bbddc199d1551d96a2de7b
3.4.1: 9e1acfb51f682522ae7221a71f834472f3d9f65264e2378d24e9fa8329c7c7dd
