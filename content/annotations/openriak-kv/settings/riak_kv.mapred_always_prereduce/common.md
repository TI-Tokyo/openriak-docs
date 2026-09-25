# Description

Default choice for applying a pre-reduce step after a MapReduce map phase. A phase's explicit `do_prereduce` argument overrides this application-wide default.

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

feature: query-processing
repository: riak_kv
module: riak_kv_mrc_pipe
concept: querying

# Notes

This is the Erlang application environment key `mapred_always_prereduce` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_mrc_pipe.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_mrc_pipe.erl#L463)

# Reviewed against

3.4.0: 4841f5db64fd7245f75f123d3c6714743daf340920881556b28a10f9dda93b64
3.4.1: 1356f0da47d623d99a6021e8764eaa9aa1afd9874df64acdee30023fbc420ffb
