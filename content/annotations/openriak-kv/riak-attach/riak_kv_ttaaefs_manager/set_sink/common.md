# Metadata

command: erlang:riak_kv_ttaaefs_manager:set_sink/3
versions: 3.4.0, 3.4.1

# Summary

Set the destination HTTP endpoint for full-sync.

# Description

The endpoint must reach the destination Riak HTTP API. This sets the runtime destination; it does not establish that the destination is reachable.

# Notes

These settings affect the current node. Runtime environment changes are not a replacement for persistent configuration.

# Arguments

## Protocol

datatype: atom
required: true
repeatable: false

### Valid values

- http

### Description

Transport used by this legacy API.

## IP

datatype: string
required: true
repeatable: false

### Description

Destination host or IP address as an Erlang string, for example `"127.0.0.1"`.

## Port

datatype: integer from 1 to 65535
required: true
repeatable: false

### Description

Destination HTTP API port, for example `8098`.

# Reviewed against

3.4.0: 231b0d5697e2b28a3976aee6ef4b343ba10433cd8fed0c8250e3102879ae3fc8
3.4.1: 231b0d5697e2b28a3976aee6ef4b343ba10433cd8fed0c8250e3102879ae3fc8

# Tags

feature: full-sync
repository: riak_kv
module: riak_kv_ttaaefs_manager
concept: replica-repair
