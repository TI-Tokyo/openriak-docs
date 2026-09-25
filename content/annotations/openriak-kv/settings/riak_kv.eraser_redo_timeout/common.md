# Description

Delay used by the background eraser before retrying unsuccessful delete work. Retries recheck that all primary replicas are available before attempting the deletion again.

# Datatype

Integer

# Units

- milliseconds

# Constraints

- Expected to be a positive integer.

# Inferred default

`2000`.

# Tags

feature: deletion
repository: riak_kv
module: riak_kv_eraser
concept: scheduling, tombstones

# Notes

This is the Erlang application environment key `eraser_redo_timeout` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_eraser.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_eraser.erl#L137)

# Reviewed against

3.4.0: 527b43bcde90b30fa651ae5bf08abb51f559a2cdb0fc3b116475ff1ca25272e9
3.4.1: e248525c7bf06fc6f14b88c9b4dbf9252e582cfaf9095c7acdb6ccb1920e36e1
