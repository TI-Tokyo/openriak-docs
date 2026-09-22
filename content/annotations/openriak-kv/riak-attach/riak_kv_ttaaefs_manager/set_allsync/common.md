# Metadata

command: erlang:riak_kv_ttaaefs_manager:set_allsync/2
versions: 3.4.0, 3.4.1

# Summary

Configure full-sync using cached trees.

# Description

Set the replication factor for the local and remote clusters. This leaves automatic syncing paused; use resume/0 to enable scheduling.

# Notes

These settings affect the current node. Runtime environment changes are not a replacement for persistent configuration.

# Arguments

## LocalNVal

datatype: positive integer
required: true
repeatable: false

### Description

Replication factor of the local data being compared, for example `3`.

## RemoteNVal

datatype: positive integer
required: true
repeatable: false

### Description

Replication factor used by the destination, for example `3`.

# Reviewed against

3.4.0: 54b2af46098ceae61817846d3cd1251659af08aa845776bd245180487bb76f6f
3.4.1: 54b2af46098ceae61817846d3cd1251659af08aa845776bd245180487bb76f6f
