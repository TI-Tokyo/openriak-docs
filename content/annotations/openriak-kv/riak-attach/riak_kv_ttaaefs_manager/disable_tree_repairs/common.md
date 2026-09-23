# Metadata

command: erlang:riak_kv_ttaaefs_manager:disable_tree_repairs/0
versions: 3.4.0, 3.4.1

# Summary

Disable repairs triggered while fetching AAE clocks.

# Description

Updates the node’s runtime environment. This does not disable all anti-entropy activity.

# Notes

These settings affect the current node. Runtime environment changes are not a replacement for persistent configuration.

# Arguments

# Reviewed against

3.4.0: 8b1b70f659f84d90754c1abf8d6ed36c9b724c7fbaf131fb38ce391db701f37e
3.4.1: 8b1b70f659f84d90754c1abf8d6ed36c9b724c7fbaf131fb38ce391db701f37e

# Tags

feature: full-sync
repository: riak_kv
module: riak_kv_ttaaefs_manager
concept: replica-repair
