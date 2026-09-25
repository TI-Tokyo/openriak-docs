# Description

Controls replication of live Riak CS bucket-metadata objects through the CS replication helper. This applies to both full-sync and realtime helper decisions; non-block tombstones are excluded separately.

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

This is the Erlang application environment key `replicate_cs_bucket_objects` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_cs.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_cs.erl#L93)

# Reviewed against

3.4.0: adc51031137b2dff47907bf1e7c0a80c7b59aa0be83c6d6cbe1a653df046dcfc
3.4.1: adc51031137b2dff47907bf1e7c0a80c7b59aa0be83c6d6cbe1a653df046dcfc
