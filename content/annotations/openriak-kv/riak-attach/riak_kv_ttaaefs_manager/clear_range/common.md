# Metadata

command: erlang:riak_kv_ttaaefs_manager:clear_range/0
versions: 3.4.0, 3.4.1

# Summary

Clear the remembered full-sync range.

# Description

Subsequent checks no longer use the previous range constraint.

# Notes

These settings affect the current node. Runtime environment changes are not a replacement for persistent configuration.

# Arguments

# Reviewed against

3.4.0: aaf22fb006dcd59b62d0dca002e24de1c7ecb06dd2cbcb4cc71c34973899af3c
3.4.1: aaf22fb006dcd59b62d0dca002e24de1c7ecb06dd2cbcb4cc71c34973899af3c

# Tags

feature: full-sync
repository: riak_kv
module: riak_kv_ttaaefs_manager
concept: replica-repair
