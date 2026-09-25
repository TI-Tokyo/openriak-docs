# Description

Optional receive socket-buffer size, in bytes, for replication connections configured by the shared socket helper. Only positive integers add a `recbuf` override.

# Datatype

Integer

# Units

- bytes

# Constraints

- Only integers greater than zero are applied; other values are ignored.

# Inferred default

Unset; leave the transport/OS socket buffer unchanged.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_util
concept: connections, memory

# Notes

This is the Erlang application environment key `recbuf` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_util.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_util.erl#L673)

# Reviewed against

3.4.0: ee0e617a295b0a44806ae203acb05077b5f955e7a56bff2dbd111f3c18d94367
3.4.1: ee0e617a295b0a44806ae203acb05077b5f955e7a56bff2dbd111f3c18d94367
