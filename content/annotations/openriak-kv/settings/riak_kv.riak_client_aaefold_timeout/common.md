# Description

Timeout, in milliseconds, for `riak_client:aae_fold/2`. It is passed to the cluster AAE fold state machine and bounds the client's wait for fold results.

# Datatype

Timeout

# Units

- milliseconds

# Constraints

- Non-negative integer fold timeout, or `infinity`.

# Inferred default

`3600000` (one hour).

# Tags

feature: tictac-aae
repository: riak_kv
module: riak_client
concept: querying, replica-repair

# Notes

This is the Erlang application environment key `riak_client_aaefold_timeout` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_client.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_client.erl#L940)

# Reviewed against

3.4.0: fc161774d44825190bea7201bb77ff1d129f08439226f446c036acbd67c4e6ad
3.4.1: fbb804ef00e46c2be9669f54d9e54d88af24c78251280cc4c33e207441dcee33
