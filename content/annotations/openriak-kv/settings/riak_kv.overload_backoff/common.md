# Description

Optional sleep, in milliseconds, before the local Riak client returns an `overload` error to its caller. It slows clients receiving overload responses without automatically retrying the operation.

# Datatype

Integer or atom

# Units

- milliseconds

# Constraints

- Non-negative integer milliseconds or `undefined`. Although the read guard accepts any number, the subsequent `timer:sleep/1` call requires an integer delay.

# Inferred default

`undefined`, so no sleep is inserted.

# Tags

feature: request-processing
repository: riak_kv
module: riak_client
concept: overload-protection

# Notes

This is the Erlang application environment key `overload_backoff` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_client.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_client.erl#L1209)

# Reviewed against

3.4.0: 1db7d4635cf2cac890446882a6e2d7487b08eac52afe8789cf8854d975c2fed3
3.4.1: ea8bae13b393fd08f1e342472ecded48d50fc8024decc3e7c76f1d6feebb0e13
