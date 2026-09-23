# Metadata

command: erlang:riak_client:aae_fold/1:repair_keys_range
versions: 3.4.0, 3.4.1

# Summary

Request read repair for keys in a bucket range.

# Description

Runs repairs over the selected range. Restrict the range to control cluster load.

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

## Filter

datatype: atom
required: true
repeatable: false

### Valid values

- all

### Description

The final selector in this API is the atom all.

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

## erlang-riak-client-aae-fold-repair-keys-range:seed-five-objects

title: Create five objects

### Description

Create five objects to follow the range-query examples. Wait for AAE to include all five before checking counts or applying a range operation.

## erlang-riak-client-aae-fold-repair-keys-range:repair-five

### Description

Request repair for a range containing five keys. The result reports processing of the range; read the objects afterward to check their availability. A successful request alone does not establish that any replica needed repair.

# Reviewed against

3.4.0: 1a73ae3d816e2685fac5799d6f1c1b2b3dd24835d12b6f5e7a54d84e555cc4e5
3.4.1: 1a73ae3d816e2685fac5799d6f1c1b2b3dd24835d12b6f5e7a54d84e555cc4e5

# Tags

feature: tictac-aae
repository: riak_kv
module: riak_client
concept: replica-repair
