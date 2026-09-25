# Description

Timeout, in milliseconds, for the handoff receiver's synchronous delivery of incoming data to the local vnode. It limits how long the receiver waits for the vnode to process a handoff item.

# Datatype

Timeout

# Units

- milliseconds

# Constraints

- Non-negative integer vnode call timeout, or `infinity`.

# Inferred default

`60000`.

# Tags

feature: handoff
repository: riak_core
module: riak_core_handoff_receiver
concept: partition-transfer

# Notes

This is the Erlang application environment key `handoff_receive_vnode_timeout` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_handoff_receiver.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_handoff_receiver.erl#L84)

# Reviewed against

3.4.0: 67032f9e4137115c214bb1dd5960f059549410e98b3d40973ca623f62b59bee7
3.4.1: 67032f9e4137115c214bb1dd5960f059549410e98b3d40973ca623f62b59bee7
