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

3.4.0: 8f744a711cdeb40440ccc668f9b3f8fea933836b0d358b89c156a770a839c335
3.4.1: f59e7f8076efe76585510114d3ecafef84353c587f6e249f885e292ebb0aef8d

# Tags

feature: full-sync
repository: riak_kv
module: riak_kv_ttaaefs_manager
concept: replica-repair
