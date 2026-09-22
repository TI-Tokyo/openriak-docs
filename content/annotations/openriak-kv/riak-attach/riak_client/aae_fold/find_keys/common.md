# Metadata

command: erlang:riak_client:aae_fold/1:find_keys
versions: 3.4.0, 3.4.1

# Summary

Find keys exceeding a sibling-count or object-size threshold.

# Description

Returns matching bucket/key entries and their measured value. Use this to locate unusually large or sibling-heavy objects.

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

## ModifiedRange

datatype: all or date tuple
required: true
repeatable: false

### Description

See the shared `ModifiedRange` argument on the AAE fold parent page.

## Threshold

datatype: threshold tuple
required: true
repeatable: false

### Description

Use `{sibling_count, N}` or `{object_size, Bytes}` with a positive threshold.

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

## erlang-riak-client-aae-fold-find-keys:seed-five-objects

title: Create five objects

### Description

Create five objects to follow the range-query examples. Wait for AAE to include all five before checking counts or applying a range operation.

## erlang-riak-client-aae-fold-find-keys:find-five

### Description

Count the returned entries; the selected key range contains exactly five matches.

# Reviewed against

3.4.0: d37e346a7ce464b56a6f9ef0197ca06f87f36d11621287c9982bd3561a2a5a64
3.4.1: d37e346a7ce464b56a6f9ef0197ca06f87f36d11621287c9982bd3561a2a5a64
