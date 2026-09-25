# Description

Fallback test switch for the memory backend's reset operation when `memory_backend.test` is absent. A true value permits clearing the local in-memory data, index and timestamp tables when the memory backend is selected.

# Datatype

Boolean

# Allowed values

- `true`
- `false`

# Constraints

- Only `true` enables the test reset fallback; `memory_backend.test` takes precedence.

# Inferred default

Unset (`undefined`); memory-backend reset remains disabled.

# Tags

feature: memory-backend
repository: riak_kv
module: riak_kv_memory_backend
concept: testing

# Notes

This is the Erlang application environment key `test` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_memory_backend.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_memory_backend.erl#L454)

# Reviewed against

3.4.0: 709074c5783e25ec42f1740f58f792b190e1f3682955187cdf5d51b87253f169
3.4.1: 0fe875441b1984d6326bf011b2a5ab2bcd021ce2dd11d613472a236cee482cb0
