# Metadata

command: erlang:riak_kv_ttaaefs_manager:get_range/0
versions: 3.4.0, 3.4.1

# Summary

Read the remembered full-sync range.

# Description

Returns `none` when no range is set, or the configured range tuple. The tuple shape differs between releases; use the example for your installed version.

# Notes

These settings affect the current node. Runtime environment changes are not a replacement for persistent configuration.

# Arguments

# Reviewed against

3.4.0: 8df48931681599e7ff9d57b34241ef2a67618e4c931afc78243a69811543d220
3.4.1: 5f168ef21aac76d1825e11ae846d4e7b38be4a308ece9869b82d26f85568a41a
