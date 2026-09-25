# Description

Lifetime, in seconds, of a cached calculated statistic. Requests reuse the value until it expires, then trigger a fresh calculation through the statistics worker.

# Datatype

Integer

# Units

- seconds

# Constraints

- Expected to be a non-negative integer cache lifetime.

# Inferred default

`5`.

# Tags

feature: observability
repository: riak_core
module: riak_core_stat_calc_proc
concept: diagnostics

# Notes

This is the Erlang application environment key `stat_cache_ttl` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_stat_calc_proc.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_stat_calc_proc.erl#L81)

# Reviewed against

3.4.0: ae516f0eb9b514088b75ae4525cf293ccfb8d7a109c8b351666d38aca0889aff
3.4.1: ae516f0eb9b514088b75ae4525cf293ccfb8d7a109c8b351666d38aca0889aff
