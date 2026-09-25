# Description

Flag checked by the ring-resize guard to determine whether Riak Control is enabled. A true value rejects ring resizing with `control_running`; this source read does not itself start Riak Control.

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
module: riak_core_claimant
concept: compatibility

# Notes

This is the Erlang application environment key `enabled` in `riak_control`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_claimant.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_claimant.erl#L636)

# Reviewed against

3.4.0: d0a4f5edd0cc065f66af0ad39eed9f4bf78d787469de52518104ddf44f515b45
3.4.1: 0d599f69c8f555e4ec49137faf8531eebea376077be360d5f4065e8080c30561
