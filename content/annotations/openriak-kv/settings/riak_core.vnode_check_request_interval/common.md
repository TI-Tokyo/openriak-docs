# Description

Number of proxied messages before sending a lightweight vnode ping to refresh the estimated mailbox backlog. It should be below `riak_core.vnode_check_interval`, so a reply can avoid the more expensive direct mailbox check.

# Datatype

Integer

# Units

- messages

# Constraints

- Non-negative integer message interval. If it is not below the effective check interval, the proxy substitutes half that interval.

# Inferred default

`50`.

# Tags

feature: request-processing
repository: riak_core
module: riak_core_vnode_proxy
concept: overload-protection

# Notes

This is the Erlang application environment key `vnode_check_request_interval` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_vnode_proxy.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_vnode_proxy.erl#L82)

# Reviewed against

3.4.0: 3f104299421696f56f76168e41c3f0a7992f86243e0a640c81bb037269e7229d
3.4.1: 3f104299421696f56f76168e41c3f0a7992f86243e0a640c81bb037269e7229d
