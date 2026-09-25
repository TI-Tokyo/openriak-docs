# Description

AAE controller queue-delay threshold, in milliseconds, that prompts the vnode to issue a synchronous ping and wait for progress. This applies backpressure when the anti-entropy controller falls behind writes.

# Datatype

Integer

# Units

- milliseconds

# Constraints

- Expected to be a non-negative integer.

# Inferred default

`1000`.

# Tags

feature: tictac-aae
repository: riak_kv
module: riak_kv_vnode
concept: queueing, replica-repair

# Notes

This is the Erlang application environment key `max_aae_queue_time` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_vnode.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_vnode.erl#L1022)

# Reviewed against

3.4.0: 982457f3ab8913aecdb868a4fc19813533e364e646606b17ecc5abf5e7c0940b
3.4.1: 6b26971959da5eaba446fac6a99d0d360738f79ed402db3d906765c3621b3bf8
