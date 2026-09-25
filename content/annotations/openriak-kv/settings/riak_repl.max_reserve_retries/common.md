# Description

Retry limit when a full-sync partition cannot be reserved because its remote location is unavailable. The coordinator drops the partition from the current run after the tracked retry count exceeds this limit.

# Datatype

Integer or atom

# Units

- retries

# Constraints

- Non-negative integer reservation retry limit; `infinity` also avoids the numeric limit comparison.

# Inferred default

`0`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl2_fscoordinator
concept: cross-cluster-replication

# Notes

This is the Erlang application environment key `max_reserve_retries` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl2_fscoordinator.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl2_fscoordinator.erl#L698)

Additional type/default evidence:

- [riak_repl/include/riak_repl.hrl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/include/riak_repl.hrl)

# Reviewed against

3.4.0: d1dce255b3a7b0d190619743ae70a15205e03cf4b610a199f2ca65150a00c824
3.4.1: d1dce255b3a7b0d190619743ae70a15205e03cf4b610a199f2ca65150a00c824
