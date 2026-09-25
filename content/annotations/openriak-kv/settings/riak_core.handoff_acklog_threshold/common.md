# Description

Threshold controlling how often the handoff sender logs progress as acknowledgements accumulate. It changes progress-report frequency without changing the handoff payload.

# Datatype

Integer

# Units

- acknowledgements

# Constraints

- Expected to be a positive integer acknowledgement count.

# Inferred default

`100`.

# Tags

feature: handoff
repository: riak_core
module: riak_core_handoff_sender
concept: diagnostics, partition-transfer

# Notes

This is the Erlang application environment key `handoff_acklog_threshold` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_handoff_sender.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_handoff_sender.erl#L437)

# Reviewed against

3.4.0: 1ffa1902c698c6087bb6c4c40104871d9608766c2b6f40daadaf1333e6333209
3.4.1: 1ffa1902c698c6087bb6c4c40104871d9608766c2b6f40daadaf1333e6333209
