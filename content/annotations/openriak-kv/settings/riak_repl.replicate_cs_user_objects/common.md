# Description

Controls replication of live Riak CS user-metadata objects through the CS replication helper. This applies to both full-sync and realtime helper decisions; non-block tombstones are excluded separately.

# Datatype

Boolean

# Allowed values

- `true`
- `false`

# Constraints

- Use the Erlang atoms `true` or `false`.

# Inferred default

`true`.

# Tags

feature: riak-cs
repository: riak_repl
module: riak_repl_cs
concept: cross-cluster-replication

# Notes

This is the Erlang application environment key `replicate_cs_user_objects` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_cs.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_cs.erl#L91)

# Reviewed against

3.4.0: 1b01d0af45ff2bf4ac8a7ec89c9412a42db57016da6d4f3e77602d9acdc6cfdc
3.4.1: 1b01d0af45ff2bf4ac8a7ec89c9412a42db57016da6d4f3e77602d9acdc6cfdc
