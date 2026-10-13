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

3.4.0: ac94fda8a53ad6fa68ac214d38c947a287dfcdd44bd7f9b1c336c55fbd0717b8
3.4.1: ac94fda8a53ad6fa68ac214d38c947a287dfcdd44bd7f9b1c336c55fbd0717b8

# Tags

feature: full-sync
repository: riak_kv
module: riak_kv_ttaaefs_manager
concept: replica-repair
