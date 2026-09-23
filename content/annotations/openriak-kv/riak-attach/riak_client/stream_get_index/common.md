# Metadata

command: erlang:riak_client:stream_get_index/3
versions: 3.4.0, 3.4.1

# Summary

Stream secondary-index results to the caller.

# Description

Returns `{ok, ReqId, CoordinatorPid}` immediately. Collect `{ReqId, {results, Keys}}` batches until `{ReqId, done}`; handle error messages and set a receiver timeout. The request handle alone does not contain the matching keys. The populated example stores five indexed objects and collects all five keys.

# Arguments

## Bucket

datatype: binary or pair of binaries
required: true
repeatable: false

### Description

See the shared `Bucket` argument on the parent module page.

## Query

datatype: secondary-index query tuple
required: true
repeatable: false

### Description

Secondary-index query, such as `{eq, <<"tag_bin">>, <<"blue">>}` or `{range, <<"age_int">>, 18, 30}`. Use an index supported by the backend.

## Opts

datatype: option list
required: false
repeatable: false

### Description

Options for the four-argument form:

- `{timeout, Milliseconds}` limits the request; the default is 60000 milliseconds.
- `{max_results, Count}` caps the result count; `all` is the default.
- `{pagination_sort, true | false}` requests sorted pagination behavior. Omit it to leave the decision to the index FSM.

For example, `[{timeout, 5000}, {max_results, 100}, {pagination_sort, true}]`. Query bounds, return-term selection and continuation belong to the index query definition, not arbitrary extra options in this list.

## Client

datatype: riak_client handle
required: true
repeatable: false

### Description

See the shared `Client` argument on the parent module page.

# Errors

## reference-error-1

### Condition

The backend does not support the requested index operation, or the coverage request times out.

### Description

The request returns an error instead of an index result.

### Remedy

Confirm backend/index support and schema, inspect node availability, and choose an appropriate timeout.

# Examples

## erlang-riak-client-stream-get-index:an-equality-query

### Description

Query an index value with no matching objects. Expect an empty result for a synchronous query; a streaming query returns a request handle followed by result messages.

# Reviewed against

3.4.0: d187a907daf5b0e8ce92db2cf7cd87f4458752f74a59b635392ed183ecd514fe
3.4.1: d187a907daf5b0e8ce92db2cf7cd87f4458752f74a59b635392ed183ecd514fe

# Tags

feature: secondary-indexes
repository: riak_kv
module: riak_client
concept: querying
