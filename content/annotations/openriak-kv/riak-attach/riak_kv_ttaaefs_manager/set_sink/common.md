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

3.4.0: b1f81acc3f9ed63c8963c249dadf4ceb25dfdc969d22710119b0790216610ee4
3.4.1: b1f81acc3f9ed63c8963c249dadf4ceb25dfdc969d22710119b0790216610ee4

# Tags

feature: full-sync
repository: riak_kv
module: riak_kv_ttaaefs_manager
concept: replica-repair
