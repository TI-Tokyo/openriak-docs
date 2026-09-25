# Description

Adds the exception stack trace to warning logs when a next-generation replication sink worker fails. The ordinary failure warning is emitted regardless of this setting.

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

feature: queue-replication
repository: riak_kv
module: riak_kv_replrtq_snk
concept: diagnostics, cross-cluster-replication

# Notes

This is the Erlang application environment key `log_snk_stacktrace` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_replrtq_snk.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_replrtq_snk.erl#L782)

# Reviewed against

3.4.0: 81afb6b3f79c3211b6e9729436a8f2b8ecac97728921477a44e5c732f657964c
3.4.1: c1936f21d0a436efd70908bc50d423967650b0b431131b2514515550c47f9971
