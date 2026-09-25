# Description

When set to `on`, percent-decodes URL values handled by the KV HTTP utility. Otherwise decoding is enabled only for requests carrying `X-Riak-URL-Encoding: on`.

# Datatype

Atom

# Allowed values

- `on`
- `off`

# Constraints

- `on` forces decoding. Other values (conventionally `off`) leave the decision to the request header.

# Inferred default

`on` from `riak_kv.app.src`. If unset, decoding depends on the request's `X-Riak-URL-Encoding` header.

# Tags

feature: client-networking
repository: riak_kv
module: riak_kv_wm_utils
concept: compatibility

# Notes

This is the Erlang application environment key `http_url_encoding` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_wm_utils.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_wm_utils.erl#L58)

Additional type/default evidence:

- [riak_kv/src/riak_kv.app.src](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv.app.src)

# Reviewed against

3.4.0: 10435accd10cf08e69e00e56c346fe0f147c540bc133bd2d7ea342ac605ea8b5
3.4.1: 024f3c9cd0e97f447aae5bae68ae1b8aae9a1f8a7f9bb045a0e621ea9db91bcf
