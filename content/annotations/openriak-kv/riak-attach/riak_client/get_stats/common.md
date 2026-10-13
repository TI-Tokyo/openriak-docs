# Metadata

command: erlang:riak_client:get_stats/2
versions: 3.4.0, 3.4.1

# Summary

Read local or cluster-wide node statistics.

# Description

Returns a list of `{Node, Statistics}` pairs. A remote RPC failure can appear inside the result; inspect each node entry. 

# Arguments

## Scope

datatype: atom
required: true
repeatable: false

### Valid values

- local
- global

### Description

Choose the client’s node or every ring member.

## Client

datatype: riak_client handle
required: true
repeatable: false

### Description

See the shared `Client` argument on the parent module page.

# Results

## outcome

### Description

The API is intended to return per-node statistics. In these packaged runtimes, the underlying riak_kv_stat:get_stats/0 call is unavailable; the result contains badrpc/undef entries. Use riak admin status for available node statistics.

# Reviewed against

3.4.0: 70c10618fe5f645648c58508bcdfef54dfba690629fd4ae59bde79aed67a8c9b
3.4.1: 70c10618fe5f645648c58508bcdfef54dfba690629fd4ae59bde79aed67a8c9b

# Tags

feature: client-operations
repository: riak_kv
module: riak_client
concept: data-access, diagnostics
