# Description

Number of replication bandwidth history entries exposed by the compatibility statistics interface. It controls how many recorded readings are returned.

# Datatype

Integer

# Units

- samples

# Constraints

- Expected to be a non-negative integer history count.

# Inferred default

`8`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_stats
concept: diagnostics

# Notes

This is the Erlang application environment key `bw_history_len` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_stats.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_stats.erl#L301)

# Reviewed against

3.4.0: 846a91a997a75c8ad59207f8e2f5484b05fb3a4fe8725fed7dcac99219984348
3.4.1: 846a91a997a75c8ad59207f8e2f5484b05fb3a4fe8725fed7dcac99219984348
