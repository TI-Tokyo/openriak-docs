# Metadata

command: erlang:riak_client:stream_list_keys/2
versions: 3.4.0, 3.4.1

# Summary

Stream bucket keys to an Erlang process.

# Description

Returns a request identifier immediately. For `{ReqId, From, {keys, Keys}}` messages, call `riak_kv_keys_fsm:ack_keys(From)` before waiting for the next batch. Messages without `From` do not need acknowledgment. Receive messages tagged with that identifier until `{ReqId, done}`; do not interpret the initial acknowledgment as the complete list.

# Notes

Listings scan cluster data and can be expensive. Use a selective indexed query when appropriate.

# Arguments

## Bucket

datatype: binary or pair of binaries
required: true
repeatable: false

### Description

See the shared `Bucket` argument on the parent module page.

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

## Input

datatype: bucket or filtered bucket tuple
required: false
repeatable: false

### Description

In the four-argument form, supply Bucket directly, or `{Bucket, FilterExpressions}` for a MapReduce-style key filter. A typed bucket such as `{<<"cli_examples">>, <<"orders">>}` is a bucket, not a filter pair; its second element is a binary.

# Errors

## reference-error-1

### Condition

The listing or receiver wait times out.

### Description

A timeout error is returned or received instead of a completion marker.

### Remedy

Check node load and the requested range. Handle timeout messages and bound how long the receiver waits.

# Reviewed against

3.4.0: 7d7a11d2b65a207dc7c99e3d8922aee5db3469c1bd954979628c87037a2e6d72
3.4.1: 7d7a11d2b65a207dc7c99e3d8922aee5db3469c1bd954979628c87037a2e6d72

# Tags

feature: query-processing
repository: riak_kv
module: riak_client
concept: querying
