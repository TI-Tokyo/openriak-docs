# Description

Uses the older full-sync coordinator reply format for unavailable or busy partitions, omitting the node field from `location_down` and `location_busy` messages. It is a compatibility switch for older replication peers.

# Datatype

Boolean

# Allowed values

- `true`
- `false`

# Constraints

- Use the Erlang atoms `true` or `false`.

# Inferred default

`false`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl2_fscoordinator_serv
concept: compatibility, cross-cluster-replication

# Notes

This is the Erlang application environment key `anya_fs_compat` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl2_fscoordinator_serv.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl2_fscoordinator_serv.erl#L167)

# Reviewed against

3.4.0: e2c61e54e9a6b0f5be62c86b0b9f45c8f2544b4ab784604e67cd3c80432b5120
3.4.1: e2c61e54e9a6b0f5be62c86b0b9f45c8f2544b4ab784604e67cd3c80432b5120
