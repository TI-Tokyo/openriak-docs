# Description

Controls forwarding of received realtime replication objects to downstream clusters. `always` places received objects on the local outgoing realtime queue; `never` suppresses that cascade.

# Datatype

Enum

# Allowed values

- `always`
- `never`

# Constraints

- The consumer accepts only these atoms.

# Inferred default

`always`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl2_rtsink_conn, riak_repl_console
concept: cross-cluster-replication

# Notes

This is the Erlang application environment key `realtime_cascades` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl2_rtsink_conn.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl2_rtsink_conn.erl#L296)
- [riak_repl/src/riak_repl_console.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_console.erl#L519)

# Reviewed against

3.4.0: da4b7e3f8399fe7b181ded9d1745b919982bbeb37e82d4b171ab94952922e4c7
3.4.1: da4b7e3f8399fe7b181ded9d1745b919982bbeb37e82d4b171ab94952922e4c7
