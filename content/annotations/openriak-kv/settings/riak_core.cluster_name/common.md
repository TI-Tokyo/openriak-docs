# Description

String included in persisted ring filenames and used to find and prune this node's ring snapshots. It identifies the ring files to load; it is distinct from the cluster identity maintained in ring metadata.

# Datatype

String

# Constraints

- Erlang character list used as the cluster component in ring filenames.

# Inferred default

`"default"` from `riak_core.app.src`.

# Tags

feature: cluster-management
repository: riak_core
module: riak_core_ring_manager
concept: filesystem-layout

# Notes

This is the Erlang application environment key `cluster_name` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_ring_manager.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_ring_manager.erl#L246)

Additional type/default evidence:

- [riak_core/src/riak_core.app.src](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core.app.src)

# Reviewed against

3.4.0: 88bf1c30701dd6a0a08419979ac2dcfbdac26ab59486c2e85c52e1e0d3f92a8b
3.4.1: 88bf1c30701dd6a0a08419979ac2dcfbdac26ab59486c2e85c52e1e0d3f92a8b
