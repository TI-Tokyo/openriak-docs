# Description

Timeout, in milliseconds, for the realtime source connection to collect its helper's status. The fallback is `status_timeout` minus one second, leaving time to return the combined status response.

# Datatype

Timeout

# Units

- milliseconds

# Constraints

- Non-negative integer timeout, or an explicit `infinity`. The computed fallback requires a numeric outer timeout of at least `1000`.

# Inferred default

`riak_repl.status_timeout - 1000`, giving `4000` when the outer timeout uses its `5000` fallback.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl2_rtsource_conn
concept: diagnostics

# Notes

This is the Erlang application environment key `status_helper_timeout` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl2_rtsource_conn.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl2_rtsource_conn.erl#L198)

# Reviewed against

3.4.0: ee7de428a9792959d4e86e749a829785eb891f105340335207b31c1b9e11cbf2
3.4.1: ee7de428a9792959d4e86e749a829785eb891f105340335207b31c1b9e11cbf2
