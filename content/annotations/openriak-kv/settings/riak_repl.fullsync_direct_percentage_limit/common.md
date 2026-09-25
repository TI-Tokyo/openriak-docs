# Description

Percentage of estimated partition keys used to calculate the direct-fetch threshold for AAE full-sync. The effective threshold is `max(fullsync_direct_limit, EstimatedKeys * Percentage div 100)` before a Bloom-filter fold is used.

# Datatype

Integer

# Units

- percent

# Constraints

- Integer percentage; `0..100` is the meaningful percentage range, but the reader does not enforce those bounds.

# Inferred default

`5`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_aae_source
concept: cross-cluster-replication, storage

# Notes

This is the Erlang application environment key `fullsync_direct_percentage_limit` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_aae_source.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_aae_source.erl#L305)

# Reviewed against

3.4.0: 782c6a2336940855a02abe7b3b17633630ec2ec7e026133316fb473098490e2c
3.4.1: 782c6a2336940855a02abe7b3b17633630ec2ec7e026133316fb473098490e2c
