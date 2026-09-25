# Description

Minimum absolute threshold of differing keys handled by direct object fetches during an AAE full-sync exchange before switching to a Bloom-filter fold. The effective threshold is the larger of this count and the configured percentage of estimated keys.

# Datatype

Integer

# Units

- objects

# Constraints

- Expected to be a non-negative integer object count.

# Inferred default

`1000`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_aae_source
concept: cross-cluster-replication, storage

# Notes

This is the Erlang application environment key `fullsync_direct_limit` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_aae_source.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_aae_source.erl#L304)

# Reviewed against

3.4.0: c86fd1806c5534ffa601976be2e627ff0a59d27751f1c482f673b6a07f190804
3.4.1: c86fd1806c5534ffa601976be2e627ff0a59d27751f1c482f673b6a07f190804
