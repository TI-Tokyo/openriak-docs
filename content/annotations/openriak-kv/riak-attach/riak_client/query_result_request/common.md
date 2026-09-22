# Metadata

command: erlang:riak_client:query_result_request/2
versions: 3.4.1

# Summary

Read another batch from a buffered query result.

# Description

Use the encoded result-queue reference returned by the query service. Keep the reference with the matching bucket and consume it before the result buffer expires.

# Arguments

## ReqMap

datatype: Erlang map
required: true
repeatable: false

### Description

Map with bucket, encoded_queue_reference and max_results keys. The queue reference is returned by the query service; do not construct one manually.

## Client

datatype: riak_client handle
required: true
repeatable: false

### Description

See the shared `Client` argument on the parent module page.

# Examples

## reference-example-1

title: Read a result batch

### Invocation

```erlang
riak_client:query_result_request(#{bucket => <<"cli_reference">>, encoded_queue_reference => QueueRef, max_results => 100}, Client).
```

### Description

Bind QueueRef to the reference returned by a buffered query and Client to a Riak client handle.

### Expected output

{ok, ResultMap} for an available result buffer, or an error term.

# Errors

## reference-error-1

### Condition

A required map key is absent or the result reference is invalid/expired.

### Description

Missing keys raise badkey; unavailable result buffers return an error.

### Remedy

Use all required map keys and the original reference from the matching query. Rerun the query if its buffer expired.

# Results

## reference-result-1

### Description

Returns a partial-result map describing the next batch, or an error if the buffer cannot be read.

# Reviewed against

3.4.1: b1679e25264b0d6205cf80047177c7dfb9f8ef234b81e1ff666db48613831a22
