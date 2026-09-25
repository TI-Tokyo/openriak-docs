# Description

Byte threshold at which the handoff sender flushes a batch of encoded objects. The object-count threshold can also trigger a flush, so a batch need not reach this byte size.

# Datatype

Integer

# Units

- bytes

# Constraints

- Expected to be a positive integer batch size.

# Inferred default

`1048576` (1 MiB).

# Tags

feature: handoff
repository: riak_core
module: riak_core_handoff_sender
concept: partition-transfer, memory

# Notes

This is the Erlang application environment key `handoff_batch_threshold` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_handoff_sender.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_handoff_sender.erl#L442)

# Reviewed against

3.4.0: d3caef8b7e4256bc934c64a59ac3027632413a8684c71d4c8a4919bf94f9008c
3.4.1: d3caef8b7e4256bc934c64a59ac3027632413a8684c71d4c8a4919bf94f9008c
