# Metadata

command: erlang:riak_client:aae_fold/1:reap_tombs
versions: 3.4.0, 3.4.1

# Summary

Count or reap tombstones matching a range.

# Description

Count or permanently remove deletion tombstones in a selected range. The examples create and delete five objects, count the resulting tombstones, reap one, and verify that four remain. Reaping discards deletion evidence: perform it only after all replicas and replication sinks have received the deletion.

# Notes

The named fields belong inside the query tuple in the order shown by the type declaration. These operations read the AAE store and can impose cluster-wide load.

# Arguments

## Bucket

datatype: bucket binary or typed bucket
required: true
repeatable: false

### Description

See the shared `Bucket` argument on the parent module page.

## KeyRange

datatype: all or binary key bounds
required: true
repeatable: false

### Description

See the shared `KeyRange` argument on the AAE fold parent page.

## SegmentFilter

datatype: all or segment tuple
required: true
repeatable: false

### Description

See the shared `SegmentFilter` argument on the AAE fold parent page.

## ModifiedRange

datatype: all or date tuple
required: true
repeatable: false

### Description

See the shared `ModifiedRange` argument on the AAE fold parent page.

## ChangeMethod

datatype: change method
required: true
repeatable: false

### Valid values

- count
- local
- {job, JobId}

### Description

See the shared `ChangeMethod` argument on the AAE fold parent page.

## Client

datatype: riak_client handle
required: false
repeatable: false

### Description

See the shared `Client` argument on the parent module page.

# Errors

## reference-error-1

### Condition

The cluster-wide fold does not finish within its timeout.

### Description

The API can return `{error, timeout}` or another error term from its coverage workers.

### Remedy

Check node availability, AAE state and filter size. Reduce the range before retrying a costly operation.

# Examples

## erlang-riak-client-aae-fold-reap-tombs:seed-five-objects

title: Create five objects

### Description

Create five objects to follow the range-query examples. Wait for AAE to include all five before checking counts or applying a range operation.

## erlang-riak-client-aae-fold-reap-tombs:create-five-tombstones

### Description

Delete the stored objects and wait until five tombstones are visible. Reaping removes these deletion markers.

# Reviewed against

3.4.0: d47b1a12261aa01297cb31c0e6ab9a8faa9a4db6e1f5fc42f8f009b6549fdc5a
3.4.1: d47b1a12261aa01297cb31c0e6ab9a8faa9a4db6e1f5fc42f8f009b6549fdc5a

# Tags

feature: tictac-aae
repository: riak_kv
module: riak_client
concept: replica-repair
