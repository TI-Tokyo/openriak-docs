# Description

Maximum pending realtime sink work used to apply socket backpressure. When too much received work awaits completion, the sink pauses socket reads until acknowledgements reduce the backlog.

# Datatype

Integer

# Units

- objects

# Constraints

- Expected to be a positive integer pending-object limit.

# Inferred default

`100`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl2_rtsink_conn
concept: queueing, cross-cluster-replication

# Notes

This is the Erlang application environment key `rtsink_max_pending` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl2_rtsink_conn.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl2_rtsink_conn.erl#L116)

# Reviewed against

3.4.0: 803accb65d43d6881371f1b48b9139865318eb01b1303197ff065ede6fb10c35
3.4.1: 803accb65d43d6881371f1b48b9139865318eb01b1303197ff065ede6fb10c35
