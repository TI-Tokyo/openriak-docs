# Description

Controls realtime replication of live Riak CS block objects through the CS replication helper. Live blocks remain eligible for full-sync independently of this switch; block tombstones have separate controls.

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

feature: riak-cs
repository: riak_repl
module: riak_repl_cs
concept: cross-cluster-replication

# Notes

This is the Erlang application environment key `replicate_cs_blocks_realtime` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_cs.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_cs.erl#L72)

# Reviewed against

3.4.0: 22bd1c4987238e9a53c5690f0721ba1670876e5b54b5abdfe9d7508dbbb50584
3.4.1: 22bd1c4987238e9a53c5690f0721ba1670876e5b54b5abdfe9d7508dbbb50584
