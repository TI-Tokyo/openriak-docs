# Description

Enables the memory backend's test reset operation when set to `true` and the selected storage backend is `riak_kv_memory_backend`. Reset clears the local backend's data, index and timestamp ETS tables. The fallback is `riak_kv.test`; this is a destructive test facility.

# Datatype

Boolean

# Allowed values

- `true`
- `false`

# Constraints

- Only `true` enables reset, and only with the memory storage backend; other values disable it.

# Inferred default

Falls back to `riak_kv.test`; if both keys are unset, reset is disabled.

# Tags

feature: memory-backend
repository: riak_kv
module: riak_kv_memory_backend
concept: testing

# Notes

This is the Erlang application environment key `test` in `memory_backend`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_memory_backend.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_memory_backend.erl#L454)

# Reviewed against

3.4.0: 9f31da4a5953ca0efebb45a0aab2731b95cb546352bfe614caf1e5b09ba04e5b
3.4.1: 42f8357edc27dc9757ef524a0d0ce974e5986b70720d7cd3aea91afc016e8885
