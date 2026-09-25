# Description

Choose how long delete tombstones remain: `keep` retains them for explicit reaping, `immediate` removes them immediately, and an integer number of milliseconds delays removal. Retaining tombstones allows deletes to reach replicas and connected clusters; early removal can allow older copies to reappear. Use a consistent policy across reconciling clusters.

# Units

- milliseconds

# Constraints

- The Cuttlefish validator accepts `keep`, `immediate`, or an integer from 1 through 299999 milliseconds. Both 0 and 300000 are excluded by the strict comparisons in the validator.
- Other positive integer delays require `advanced.config`, which bypasses this schema validator.

# Notes

Checked against the [delete-mode schema validator](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/priv/riak_kv.schema#L1744). Its error message says "between 0 and 300000", but the implementation uses `Value > 0` and `Value < 300000`. The same checks apply in 3.4.0 and 3.4.1.

# Tags

feature: deletion
repository: riak_kv
module: riak_kv_eraser, riak_kv_vnode
concept: retention, tombstones

# Reviewed against

3.4.0: 148abb6a6d68fe51bb3e7f6d2b1d1b15a6be7458f3d77426a4f9acee1ef7d813
3.4.1: acb9fc516294d76f052077d339d032470bc9c75e711855a718e18ca9f0f8d6c7
