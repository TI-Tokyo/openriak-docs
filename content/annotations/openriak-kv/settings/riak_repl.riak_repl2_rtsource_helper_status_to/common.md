# Description

Default timeout, in milliseconds, for direct status requests to a realtime source helper. Callers that supply an explicit timeout, including the source connection's status aggregation, override it.

# Datatype

Timeout

# Units

- milliseconds

# Constraints

- Non-negative integer helper call timeout, or `infinity`.

# Inferred default

`120000`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl2_rtsource_helper
concept: diagnostics

# Notes

This is the Erlang application environment key `riak_repl2_rtsource_helper_status_to` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl2_rtsource_helper.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl2_rtsource_helper.erl#L48)

Additional type/default evidence:

- [riak_repl/include/riak_repl.hrl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/include/riak_repl.hrl)

# Reviewed against

3.4.0: d170151b50d73ceeef9678684fecae4c273fc3e8c57c72142fb32533e9ad503f
3.4.1: d170151b50d73ceeef9678684fecae4c273fc3e8c57c72142fb32533e9ad503f
