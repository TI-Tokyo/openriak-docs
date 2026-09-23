# Metadata

command: erlang:riak_client:ttaaefs_fullsync/1
versions: 3.4.0, 3.4.1

# Summary

Run a full-sync work item using the current manager configuration.

# Description

Choose a work item compatible with the configured sync mode. `null_check` performs no data comparison. Other work items require a configured destination.

# Arguments

## WorkItem

datatype: atom
required: true
repeatable: false

### Valid values

- null_check
- all_check
- hour_check
- day_check
- range_check
- auto_check

### Description

Type of check to request.

## SecsTimeout

datatype: non-negative integer
required: false
repeatable: false
default: 900

### Description

Time to wait for the result, in seconds. The one-argument form uses 900.

## Now

datatype: Erlang timestamp tuple
required: false
repeatable: false

### Description

Reference timestamp for the check. Normally omitted so the current timestamp is used.

# Results

## outcome

### Description

A completed check returns a comparison result; a timed-out check returns {error,timeout}. The bounded null-check example exercises the timeout path, not a successful exchange with another cluster.

# Examples

## erlang-riak-client-ttaaefs-fullsync:seed-five-objects

title: Create five objects

### Description

Create five objects to follow the range-query examples. Wait for AAE to include all five before checking counts or applying a range operation.

# Reviewed against

3.4.0: d115a5d7df27e3fc897d91d1832a8ec65b3c5d4e5d12f4d08d9b9dc55bd4c331
3.4.1: d115a5d7df27e3fc897d91d1832a8ec65b3c5d4e5d12f4d08d9b9dc55bd4c331

# Tags

feature: full-sync
repository: riak_kv
module: riak_client
concept: replica-repair
