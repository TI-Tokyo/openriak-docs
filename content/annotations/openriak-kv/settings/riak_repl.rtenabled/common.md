# Description

Internal flag reflecting whether realtime replication is enabled. Replication management updates it from the configured state, and write hooks consult it together with bucket properties before enqueueing objects.

# Datatype

Boolean

# Allowed values

- `true`
- `false`

# Constraints

- Use the Erlang atoms `true` or `false`.

# Inferred default

`false`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl, riak_repl_ring_handler, riak_repl_rtenqueue
concept: cross-cluster-replication, runtime

# Notes

This is the Erlang application environment key `rtenabled` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl.erl#L38)
- [riak_repl/src/riak_repl_ring_handler.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_ring_handler.erl#L166)
- [riak_repl/src/riak_repl_rtenqueue.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_rtenqueue.erl#L65)

# Reviewed against

3.4.0: d81577c688ece3adf4b7e3826db8addfb94b6500d3636d41fbcfae79e77dc26b
3.4.1: d81577c688ece3adf4b7e3826db8addfb94b6500d3636d41fbcfae79e77dc26b
