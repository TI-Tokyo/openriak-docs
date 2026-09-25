# Description

Wait budget for draining the realtime replication queue before attempting to migrate remaining entries to another replication node. The implementation compares this value with a millisecond counter advanced by its polling loop; it is not the timeout of the outer synchronous call.

# Datatype

Integer

# Units

- seconds

# Constraints

- Expected to be a non-negative numeric wait budget; `infinity` is not supported by the migration interface.

# Inferred default

`5`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_migration
concept: queueing, cross-cluster-replication

# Notes

This is the Erlang application environment key `queue_migration_timeout` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_migration.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_migration.erl#L26)

# Reviewed against

3.4.0: 44010308496d8b51316e3954a291db86b11b515ff32a162360a1d138de42c856
3.4.1: 44010308496d8b51316e3954a291db86b11b515ff32a162360a1d138de42c856
