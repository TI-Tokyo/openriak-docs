# Description

Interval, in seconds, between progress updates sent by an active handoff sender to the handoff manager. It controls the refresh rate of transfer statistics.

# Datatype

Integer

# Units

- seconds

# Constraints

- Positive integer reporting interval according to the helper specification.

# Inferred default

`2`.

# Tags

feature: handoff
repository: riak_core
module: riak_core_handoff_sender
concept: diagnostics, partition-transfer

# Notes

This is the Erlang application environment key `handoff_status_interval` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_handoff_sender.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_handoff_sender.erl#L778)

# Reviewed against

3.4.0: a897e95570830cbc9f4162125fddc2abe407e4ee4db92c98aad21f044092a63d
3.4.1: a897e95570830cbc9f4162125fddc2abe407e4ee4db92c98aad21f044092a63d
