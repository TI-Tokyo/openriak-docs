# Metadata

command: erlang:riak_client:query/2
versions: 3.4.0, 3.4.1

# Summary

Run a structured query through the KV query service.

# Description

Build the query with riak_kv_query functions, check each validation result, then submit it with a client handle. Results can be immediate or refer to a result queue.

# Arguments

## Query

datatype: validated query record
required: true
repeatable: false

### Description

Validated riak_kv_query record. Construct it with new/4 and add_queries/3 rather than assembling the internal record tuple.

## Client

datatype: riak_client handle
required: true
repeatable: false

### Description

See the shared `Client` argument on the parent module page.

# Errors

## reference-error-1

### Condition

Query validation fails or the query service times out.

### Description

Builders return `{error, Stage, Message}`; execution can return `{error, timeout}` or another error term.

### Remedy

Inspect each builder result before submitting and correct the reported stage; check backend support and query load.

# Reviewed against

3.4.0: 17afad7800669525b6b63bfa7ed5e49195bc62c22a69ff0e65e72914b9db7684
3.4.1: 0851593cbb71b43bead1d3c99997d01026e7cbd01515096fdca9e2199ddd6369

# Tags

feature: client-operations
repository: riak_kv
module: riak_client
concept: data-access
