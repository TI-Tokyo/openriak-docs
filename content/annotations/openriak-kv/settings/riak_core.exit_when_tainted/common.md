# Description

Controls the response when a ring marked as tainted reaches a protected operation. When true, Riak stops the node; when false, it logs the error and continues.

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

feature: cluster-management
repository: riak_core
module: riak_core_ring
concept: diagnostics

# Notes

This is the Erlang application environment key `exit_when_tainted` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_ring.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_ring.erl#L268)

# Reviewed against

3.4.0: 91ccee1e97dfbfa7f99cb61c2687939b32aa00ac5cccff99029256177b911494
3.4.1: 91ccee1e97dfbfa7f99cb61c2687939b32aa00ac5cccff99029256177b911494
