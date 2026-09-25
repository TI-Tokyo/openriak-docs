# Description

`{Low, High}` vnode mailbox watermarks used by KV's optional health check. An active service is judged against the high watermark; a disabled service must recover below the low watermark before becoming healthy again.

# Datatype

Tuple

# Constraints

- `{LowWatermark, HighWatermark}` using non-negative integer mailbox lengths; normally `LowWatermark <= HighWatermark`.

# Inferred default

`{1, 5000}`.

# Tags

feature: object-storage
repository: riak_kv
module: riak_kv_app
concept: diagnostics, overload-protection

# Notes

This is the Erlang application environment key `vnode_mailbox_limit` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_app.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_app.erl#L327)

# Reviewed against

3.4.0: 7dca3325050140d5d0c03d8e4fdc43afa17ff80490658a8ff2f22b71a712e6e1
3.4.1: 586e7805d36ec5f9bc02415f36354410598601f12b341c682156cadf2a4a65a2
