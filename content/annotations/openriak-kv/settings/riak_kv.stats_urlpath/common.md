# Description

HTTP path component used for the statistics endpoint. The source fallback is `stats`, producing the `/stats` route.

# Datatype

String

# Constraints

- Erlang character list used as the HTTP statistics route prefix.

# Inferred default

`"stats"`.

# Tags

feature: observability
repository: riak_kv
module: riak_kv_web
concept: diagnostics

# Notes

This is the Erlang application environment key `stats_urlpath` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_web.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_web.erl#L197)

Additional type/default evidence:

- [riak_kv/src/riak_kv.app.src](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv.app.src)

# Reviewed against

3.4.0: 3c333ef07b7b3fb88e9a305c5a1a4388a360c7e9d6c3988ee3ec65a3c052ca34
3.4.1: 9f96d272b7187958b5f9b30b8b7d1cf78e33ec58f4935699e5a3d007d16655d7
