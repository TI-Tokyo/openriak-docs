# Description

Selects the older coverage-plan algorithm instead of the newer planner. This is a compatibility fallback for choosing the vnodes needed to cover a query's keyspaces and can be considerably slower on large rings.

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

feature: query-processing
repository: riak_core
module: riak_core_coverage_plan
concept: partition-placement, compatibility

# Notes

This is the Erlang application environment key `legacy_coverage_planner` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_coverage_plan.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_coverage_plan.erl#L103)

# Reviewed against

3.4.0: 673ad54ef9d52137ce5d48e7c651d08a536f42eb9693c759b1409e9dabda0d1d
3.4.1: 103fe980acd20490fce290772ee7fb072099e42520ba75aaf0a7001a8aa8a31f
