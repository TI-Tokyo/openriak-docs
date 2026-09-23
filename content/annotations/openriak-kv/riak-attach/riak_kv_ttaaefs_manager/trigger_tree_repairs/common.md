# Metadata

command: erlang:riak_kv_ttaaefs_manager:trigger_tree_repairs/0
versions: 3.4.0, 3.4.1

# Summary

Enable tree repair tracking for the current process.

# Description

Initialises the repair count and records the caller as the repair-tracking process. Call from an administrative shell that remains alive during the operation.

# Notes

These settings affect the current node. Runtime environment changes are not a replacement for persistent configuration.

# Arguments

# Reviewed against

3.4.0: c85c318912a9a79a99239326904948e2bc37d3b9ee54bb18c495531e138e3d5b
3.4.1: c85c318912a9a79a99239326904948e2bc37d3b9ee54bb18c495531e138e3d5b

# Tags

feature: full-sync
repository: riak_kv
module: riak_kv_ttaaefs_manager
concept: replica-repair
