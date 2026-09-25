# Description

Estimated vnode mailbox backlog above which the proxy rejects new work through the vnode's overload handlers. Setting it to `undefined` bypasses this proxy overload check.

# Datatype

Integer or atom

# Units

- messages

# Constraints

- Expected to be a positive integer mailbox threshold, or `undefined` to disable overload rejection.

# Inferred default

`10000`.

# Tags

feature: request-processing
repository: riak_core
module: riak_core_vnode_proxy
concept: overload-protection

# Notes

This is the Erlang application environment key `vnode_overload_threshold` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_vnode_proxy.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_vnode_proxy.erl#L85)

# Reviewed against

3.4.0: c4a6e8a743322bbf6febdfe5dc1a3adef0f865e78d7c98bfe4e6e5adfdc7141f
3.4.1: c4a6e8a743322bbf6febdfe5dc1a3adef0f865e78d7c98bfe4e6e5adfdc7141f
