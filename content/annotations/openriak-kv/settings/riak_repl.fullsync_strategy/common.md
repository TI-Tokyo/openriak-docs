# Description

Preferred full-sync strategy for the newer `riak_repl2` source, such as AAE or keylist comparison. The source derives its supported capabilities from this preference and can fall back when local AAE or the peer's support is unavailable.

# Datatype

Enum

# Allowed values

- `keylist`
- `aae`

# Constraints

- `aae` requires KV active anti-entropy; otherwise the consumer falls back to `keylist`.

# Inferred default

`keylist`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl2_fssource
concept: cross-cluster-replication

# Notes

This is the Erlang application environment key `fullsync_strategy` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl2_fssource.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl2_fssource.erl#L94)

Additional type/default evidence:

- [riak_repl/include/riak_repl.hrl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/include/riak_repl.hrl)

# Reviewed against

3.4.0: 8830c14e2138be04d885f40c06e536e0573545ee80d69e66b0b7e326f8ab5afd
3.4.1: 8830c14e2138be04d885f40c06e536e0573545ee80d69e66b0b7e326f8ab5afd
