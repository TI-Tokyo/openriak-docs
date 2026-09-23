# Metadata

command: erlang:riak_kv_ttaaefs_manager:autocheck_suppress/0
versions: 3.4.0, 3.4.1

# Summary

Suppress the next automatic full-sync checks.

# Description

The zero-argument form reads the configured suppress count. Supply a non-negative count to choose how many upcoming automatic checks to skip.

# Notes

These settings affect the current node. Runtime environment changes are not a replacement for persistent configuration.

# Arguments

## SuppressCount

datatype: non-negative integer
required: false
repeatable: false

### Description

Number of automatic checks to skip. The shorter arity uses the configured count.

# Reviewed against

3.4.0: 406d5b594e361cd08e241ec1679d4889b811949ce23a420b2da590f1dcb2733f
3.4.1: 406d5b594e361cd08e241ec1679d4889b811949ce23a420b2da590f1dcb2733f

# Tags

feature: full-sync
repository: riak_kv
module: riak_kv_ttaaefs_manager
concept: replica-repair
