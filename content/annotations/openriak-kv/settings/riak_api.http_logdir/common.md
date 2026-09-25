# Description

Directory passed to the HTTP server for request logging. If unset, Riak uses `riak_core.platform_log_dir`, falling back to `log`.

# Datatype

Directory path

# Constraints

- Directory name as an Erlang filename string.

# Inferred default

The value of `riak_core.platform_log_dir`, falling back to `"log"`.

# Tags

feature: client-networking
repository: riak_api
module: riak_api_web
concept: diagnostics, filesystem-layout

# Notes

This is the Erlang application environment key `http_logdir` in `riak_api`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_api/src/riak_api_web.erl](https://github.com/OpenRiak/riak_api/blob/ffdbd6be1afd3e2350eee99dc96930f7b339c3bf/src/riak_api_web.erl#L95)

# Reviewed against

3.4.0: 22fa30af754b5f6ffb48264581d810d743e96ac0341e40b0b5550bfc3b3dd4f7
3.4.1: a8072302f8dca0c36d7de5b49c07e3e1c22a4e7ffb2b559a145ff45b91876395
