# Description

Optional receive socket-buffer size, in bytes, added to Riak's HTTP and HTTPS listener options. The listener leaves the underlying default unchanged when this application value is absent.

# Datatype

Integer

# Units

- bytes

# Constraints

- Expected to be a positive integer socket receive-buffer size.

# Inferred default

Unset; the HTTP server retains its transport/OS receive-buffer default.

# Tags

feature: client-networking
repository: riak_api
module: riak_api_web
concept: connections, memory

# Notes

This is the Erlang application environment key `recbuf` in `webmachine`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_api/src/riak_api_web.erl](https://github.com/OpenRiak/riak_api/blob/ffdbd6be1afd3e2350eee99dc96930f7b339c3bf/src/riak_api_web.erl#L78)

# Reviewed against

3.4.0: ed666f00527eb41ba0854dc71f5ce7c808a3ef44ce5081a2f03b3b554064a837
3.4.1: 257eb0f5b17d48976fadcf43784158569aad9e5e07c81a4a39be6674e3b9f00c
