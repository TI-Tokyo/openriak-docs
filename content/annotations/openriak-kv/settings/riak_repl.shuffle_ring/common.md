# Description

Randomizes partition order when beginning a fresh keylist full-sync. This reduces the chance that repeated restarts continually revisit the same initial partitions; saved resume progress is used when available.

# Datatype

Boolean

# Allowed values

- `true`
- `false`

# Constraints

- Use the Erlang atoms `true` or `false`.

# Inferred default

`true`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_keylist_client
concept: scheduling, cross-cluster-replication

# Notes

This is the Erlang application environment key `shuffle_ring` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_keylist_client.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_keylist_client.erl#L79)

# Reviewed against

3.4.0: da630bb2162b3519179716164969996fbea332d56f8dda97dffe789dfbce0838
3.4.1: da630bb2162b3519179716164969996fbea332d56f8dda97dffe789dfbce0838
