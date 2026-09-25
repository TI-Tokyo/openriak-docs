# Description

Optional send socket-buffer size, in bytes, for replication connections configured by the shared socket helper. Only positive integers add a `sndbuf` override.

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

This is the Erlang application environment key `sndbuf` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_util.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_util.erl#L679)

# Reviewed against

3.4.0: c8e4fcd0bc084d92c6e59bb24b3d23b732a9dcb5878d00882f0b5056bde78e67
3.4.1: c8e4fcd0bc084d92c6e59bb24b3d23b732a9dcb5878d00882f0b5056bde78e67
