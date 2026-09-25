# Description

Controls whether the Riak CS replication helper includes block tombstones in full-sync. The source fallback excludes them to avoid repeatedly propagating lingering deleted blocks.

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
concept: cross-cluster-replication, tombstones

# Notes

This is the Erlang application environment key `replicate_cs_block_tombstone_fullsync` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_cs.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_cs.erl#L79)

# Reviewed against

3.4.0: a10a671da2182f4c8fb830fd28092e55d21dfc5f920828cf320e497fce920c82
3.4.1: a10a671da2182f4c8fb830fd28092e55d21dfc5f920828cf320e497fce920c82
