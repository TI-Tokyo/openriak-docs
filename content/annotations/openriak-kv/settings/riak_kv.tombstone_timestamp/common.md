# Description

Adds a last-modified timestamp when constructing a deletion tombstone. Disabling it retains the legacy tombstone construction path without that timestamp update.

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

feature: deletion
repository: riak_kv
module: riak_kv_delete
concept: retention, tombstones

# Notes

This is the Erlang application environment key `tombstone_timestamp` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_delete.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_delete.erl#L226)

# Reviewed against

3.4.0: 876ef715cec6f04afc4989e77cf1f22c0c6ced3cc711069dd1c3879c121e3c11
3.4.1: abfe35763a41b5c0355c600a10e6c3082a04a55f8cbdd7a0f921c730eb4b7a52
