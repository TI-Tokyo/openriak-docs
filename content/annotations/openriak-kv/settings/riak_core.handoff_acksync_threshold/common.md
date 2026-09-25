# Description

Number of handoff batches allowed between synchronous acknowledgement checks. Smaller values make the sender wait for receiver progress more frequently, limiting how far it can run ahead.

# Datatype

Integer

# Units

- acknowledgements

# Constraints

- Expected to be a positive integer acknowledgement count.

# Inferred default

`1`.

# Tags

feature: handoff
repository: riak_core
module: riak_core_handoff_sender
concept: partition-transfer

# Notes

This is the Erlang application environment key `handoff_acksync_threshold` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_handoff_sender.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_handoff_sender.erl#L430)

# Reviewed against

3.4.0: d2955440b548f6631fcb315f80ceb1b86343465b96980533ba81b99c93748dd9
3.4.1: d2955440b548f6631fcb315f80ceb1b86343465b96980533ba81b99c93748dd9
