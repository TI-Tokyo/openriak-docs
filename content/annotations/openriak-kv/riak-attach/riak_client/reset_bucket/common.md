# Metadata

command: erlang:riak_client:reset_bucket/2
versions: 3.4.0, 3.4.1

# Summary

Restore a bucket’s properties to defaults.

# Description

Removes bucket-specific overrides. Review the effective properties afterward before resuming application traffic.

# Arguments

## Bucket

datatype: binary or pair of binaries
required: true
repeatable: false

### Description

See the shared `Bucket` argument on the parent module page.

## Client

datatype: riak_client handle
required: true
repeatable: false

### Description

See the shared `Client` argument on the parent module page.

# Reviewed against

3.4.0: a113b325faa462086ca7bac2df0beecf2efba8f7231643cb9d06a2d8da98f431
3.4.1: a113b325faa462086ca7bac2df0beecf2efba8f7231643cb9d06a2d8da98f431
