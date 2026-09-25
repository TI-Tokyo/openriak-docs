# Description

Base idle interval, in milliseconds, before a vnode reports inactivity to the vnode manager, which can use the notification to drive handoff. Each vnode adds a random delay up to this value to spread notifications out.

# Datatype

Integer

# Units

- milliseconds

# Constraints

- Must be a positive integer because the code calls `rand:uniform(Timeout)`.

# Inferred default

`60000`; each vnode adds a random `1..60000` milliseconds to its timer.

# Tags

feature: cluster-management
repository: riak_core
module: riak_core_vnode
concept: scheduling, partition-transfer

# Notes

This is the Erlang application environment key `vnode_inactivity_timeout` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_vnode.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_vnode.erl#L276)

Additional type/default evidence:

- [riak_core/src/riak_core.app.src](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core.app.src)

# Reviewed against

3.4.0: e707d46689165cc8cdc516976217fb96cb7e4aebcffea15a11d8f6e95cd24bfc
3.4.1: e707d46689165cc8cdc516976217fb96cb7e4aebcffea15a11d8f6e95cd24bfc
