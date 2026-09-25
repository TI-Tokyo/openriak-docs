# Description

Chooses how direct object fetches are performed during legacy AAE full-sync. `inline` fetches as differences are found; `buffered` retains differing keys in ETS for processing after comparison, subject to the direct-fetch threshold.

# Datatype

Enum

# Allowed values

- `inline`
- `buffered`

# Constraints

- The consumer pattern-matches these two atoms.

# Inferred default

`inline`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_aae_source
concept: cross-cluster-replication, memory

# Notes

This is the Erlang application environment key `fullsync_direct_mode` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_aae_source.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_aae_source.erl#L307)

# Reviewed against

3.4.0: 1c07776b4e932b4e74bc1388f2a5ec0f06be08a45ed379d823cce3eaecefde80
3.4.1: 1c07776b4e932b4e74bc1388f2a5ec0f06be08a45ed379d823cce3eaecefde80
