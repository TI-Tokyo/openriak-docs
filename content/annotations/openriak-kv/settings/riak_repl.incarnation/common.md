# Description

Internal identifier generated each time the replication application starts. It names that run's work directory so temporary files from different application incarnations can be separated and old directories pruned.

# Datatype

Integer

# Constraints

- Non-negative integer startup identifier. Managed by the application, which overwrites it at startup.

# Inferred default

Generated at every replication application start with `erlang:phash2({make_ref(), os:timestamp()})`; no fixed value.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_app
concept: filesystem-layout, runtime

# Notes

This is the Erlang application environment key `incarnation` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_app.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_app.erl#L153)

# Reviewed against

3.4.0: 0a5a41a11d54f3000f1c92cded823a5fe0552ce75fe9d5b2e7e6c96bf4c35267
3.4.1: 0a5a41a11d54f3000f1c92cded823a5fe0552ce75fe9d5b2e7e6c96bf4c35267
