# Description

Retry limit for a partition whose full-sync source worker exits with an error. Once the tracked error count exceeds the limit, the coordinator drops that partition from the current full-sync run.

# Datatype

Integer or atom

# Units

- retries

# Constraints

- Non-negative integer retry limit, or `infinity` for no limit.

# Inferred default

`infinity`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl2_fscoordinator
concept: cross-cluster-replication

# Notes

This is the Erlang application environment key `max_fssource_retries` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl2_fscoordinator.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl2_fscoordinator.erl#L583)

Additional type/default evidence:

- [riak_repl/include/riak_repl.hrl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/include/riak_repl.hrl)

# Reviewed against

3.4.0: decfebde8f4f0a996e53e3966b619b2aed07d9d5685e103abade5ab1365a6ce2
3.4.1: decfebde8f4f0a996e53e3966b619b2aed07d9d5685e103abade5ab1365a6ce2
