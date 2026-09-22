# Metadata

command: erlang:riak_client:push/4
versions: 3.4.0, 3.4.1

# Summary

Apply an object received through replication.

# Description

This is the internal replication write path. It accepts a Riak object or next-generation replication encoding and handles deletion/reap markers separately from ordinary writes.

# Arguments

## RObjMaybeBin

datatype: riak_object or binary
required: true
repeatable: false

### Description

Riak object or its supported replication binary encoding.

## IsDeleted

datatype: boolean
required: true
repeatable: false

### Valid values

- true
- false

### Description

Whether the object is a deletion marker.

## Opts

datatype: option list
required: true
repeatable: false

### Description

Replication write options as a property list.

## Client

datatype: riak_client handle
required: true
repeatable: false

### Description

See the shared `Client` argument on the parent module page.

# Errors

## reference-error-1

### Condition

The replicated payload cannot be decoded or required replicas do not acknowledge the write.

### Description

The operation can raise a decode error or return timeout, too_many_fails or n_val_violation.

### Remedy

Verify payload provenance/encoding, replication factor and node health before retrying.

# Examples

## erlang-riak-client-push:an-ordinary-object

### Description

Apply a normal replicated object in the bucket.

# Reviewed against

3.4.0: 007723576e33fe99631c69f55fb408d8ad22569f0cacbc120562ad804294f3ef
3.4.1: 007723576e33fe99631c69f55fb408d8ad22569f0cacbc120562ad804294f3ef
