# Description

Working directory for temporary replication files and per-connection full-sync subdirectories. Replication startup normally computes and stores this path from the data root and current incarnation identifier.

# Datatype

Directory path

# Constraints

- Writable directory path; the application sets it before replication workers start.

# Inferred default

Set at replication startup to `<data_root>/work/<incarnation>`, with a newly generated incarnation.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_fsm_common
concept: filesystem-layout, runtime

# Notes

This is the Erlang application environment key `work_dir` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_fsm_common.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_fsm_common.erl#L21)

Additional type/default evidence:

- [riak_repl/src/riak_repl_app.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_app.erl)

# Reviewed against

3.4.0: 5a275f157a3a04a30f8e3497c96abfe11a86e4ce751cb0c3217ecfa4875b3360
3.4.1: 5a275f157a3a04a30f8e3497c96abfe11a86e4ce751cb0c3217ecfa4875b3360
