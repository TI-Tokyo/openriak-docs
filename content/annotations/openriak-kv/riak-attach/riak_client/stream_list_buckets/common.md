# Metadata

command: erlang:riak_client:stream_list_buckets/1
versions: 3.4.0, 3.4.1

# Summary

Stream bucket names to an Erlang process.

# Description

Returns a request identifier immediately. Receive messages tagged with that identifier until `{ReqId, done}`; do not interpret the initial acknowledgment as the complete list.

# Notes

Listings scan cluster data and can be expensive. Use a selective indexed query when appropriate.

# Arguments

## Timeout

datatype: timeout in milliseconds
required: false
repeatable: false

### Description

See the shared `Timeout` argument on the parent module page.

## Recipient

datatype: Erlang pid
required: false
repeatable: false

### Description

Optional recipient process in the longer arity; use self() for the current shell. Distinct from the Riak client handle.

## Client

datatype: riak_client handle
required: true
repeatable: false

### Description

See the shared `Client` argument on the parent module page.

## Filter

datatype: predicate or none
required: false
repeatable: false

### Description

Optional bucket-name predicate, for example `fun(B) -> B =:= <<"orders">> end`, or `none` for no filtering.

## Type

datatype: binary
required: false
repeatable: false

### Description

Bucket type as a binary, for example `<<"default">>` or the active type `<<"cli_examples">>`.

# Errors

## reference-error-1

### Condition

The listing or receiver wait times out.

### Description

A timeout error is returned or received instead of a completion marker.

### Remedy

Check node load and the requested range. Handle timeout messages and bound how long the receiver waits.

# Examples

## erlang-riak-client-stream-list-buckets:collect-a-small-stream

### Description

Collect bucket-list batches until the completion marker to avoid treating a partial stream as the full list. Stop waiting after five seconds if completion does not arrive.

# Reviewed against

3.4.0: 59b24318f48a9d7a6a3a4f268e768493c9490bbe79281a837a93552e98a4ec6c
3.4.1: 59b24318f48a9d7a6a3a4f268e768493c9490bbe79281a837a93552e98a4ec6c
