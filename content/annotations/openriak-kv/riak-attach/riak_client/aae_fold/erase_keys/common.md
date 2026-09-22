# Metadata

command: erlang:riak_client:aae_fold/1:erase_keys
versions: 3.4.0, 3.4.1

# Summary

Count or erase keys matching a range.

# Description

Count live objects in a selected bucket and key range, or erase them. Start with `count` to inspect the selection. The examples create five objects, erase one selected key, and verify that four remain. Both `local` and `{job, JobId}` methods perform deletion; poll the resulting count to check completion.

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

## erlang-riak-client-aae-fold-erase-keys:seed-five-objects

title: Create five objects

### Description

Create five objects to follow the range-query examples. Wait for AAE to include all five before checking counts or applying a range operation.

# Reviewed against

3.4.0: 3060d9c70aeec416fd3002d2913de71f6f9df91fe67dc8ac7d2ad3b5a793c74b
3.4.1: 3060d9c70aeec416fd3002d2913de71f6f9df91fe67dc8ac7d2ad3b5a793c74b
