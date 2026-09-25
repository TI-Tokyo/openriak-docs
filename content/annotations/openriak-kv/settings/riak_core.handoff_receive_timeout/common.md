# Description

Timeout, in milliseconds, for an idle handoff receiver waiting for further traffic. An expired receive timeout closes the stalled transfer.

# Datatype

Timeout

# Units

- milliseconds

# Constraints

- Non-negative integer gen_server idle timeout, or `infinity`.

# Inferred default

`300000`.

# Tags

feature: handoff
repository: riak_core
module: riak_core_handoff_receiver
concept: partition-transfer

# Notes

This is the Erlang application environment key `handoff_receive_timeout` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_handoff_receiver.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_handoff_receiver.erl#L230)

# Reviewed against

3.4.0: 901e16c55981d3b0ce7e8d151a5a54df971a29db36c9a2cffa3f54fbb5588e9e
3.4.1: 901e16c55981d3b0ce7e8d151a5a54df971a29db36c9a2cffa3f54fbb5588e9e
