# Description

Number of proxied messages between direct vnode mailbox-length checks. This is a message count, not a time interval; the proxy reduces it if necessary to keep it below the overload threshold.

# Datatype

Integer

# Units

- messages

# Constraints

- Positive integer message interval. If it is not below a configured overload threshold, the proxy substitutes half that threshold.

# Inferred default

`5000`.

# Tags

feature: request-processing
repository: riak_core
module: riak_core_vnode_proxy
concept: overload-protection

# Notes

This is the Erlang application environment key `vnode_check_interval` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_vnode_proxy.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_vnode_proxy.erl#L79)

# Reviewed against

3.4.0: 290f38dd856c96bdcba39f069330c9240bbf7fea8ef5cf9c59e87d525b4d714d
3.4.1: 290f38dd856c96bdcba39f069330c9240bbf7fea8ef5cf9c59e87d525b4d714d
