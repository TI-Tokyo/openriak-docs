# Description

Controls whether the Riak CS replication helper forwards block tombstones through realtime replication. Sending them carries deletion history to the sink and can avoid a read-before-delete operation there.

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
concept: cross-cluster-replication, tombstones

# Notes

This is the Erlang application environment key `replicate_cs_block_tombstone_realtime` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_cs.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_cs.erl#L85)

# Reviewed against

3.4.0: dae2ae3e152c855b13cf980a3ac3627570b3fe8abd16306752665765bc1e3c70
3.4.1: dae2ae3e152c855b13cf980a3ac3627570b3fe8abd16306752665765bc1e3c70
