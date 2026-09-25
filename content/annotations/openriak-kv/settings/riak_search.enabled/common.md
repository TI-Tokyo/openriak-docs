# Description

Flag checked by the ring-resize guard to determine whether legacy Riak Search is enabled. A true value rejects resizing with `search_running`; this read does not itself start a search service.

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

This is the Erlang application environment key `enabled` in `riak_search`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_claimant.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_claimant.erl#L637)

# Reviewed against

3.4.0: 49bd2c30ef096e02730d67e838ac73dd86dcb8cd86f9e2f6bd401efa355275ac
3.4.1: 09cd8a1a45ea49765c48a656e562629f9a0c575ee1c8b2913deee38c3c9fbf5c
