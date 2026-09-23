# Metadata

command: shell:riak admin cluster plan
versions: 3.4.0, 3.4.1

# Summary

Preview staged cluster changes before committing them.

# Description

Run plan after staging joins, leaves or other membership changes. It shows the proposed membership, ownership and partition movement. Review every staged action and any replica-placement warnings before committing. Running plan does not start transfers.

# Arguments

# Notes

The examples build a five-node cluster: node1 is the initial member; node2 through node5 are candidates. A successful join first leaves a candidate in `joining` state. Commit applies a reviewed plan; transfers complete afterward.

| Situation | Expected plan result |
| --- | --- |
| No joins are staged | No staged changes |
| One node has joined, with no plan yet | A join row and projected ownership for that node |
| The same join has already been planned | The same staged join is shown again |
| More nodes join after planning | A refreshed plan includes all staged joins |
| All five nodes have converged after commit | No staged changes |

A rejected join never becomes part of a plan. A cookie mismatch can therefore leave plan showing no changes, even though an attempted join failed. See the shared cluster errors below.

# Related documentation

- [Stage a join](../join/)
- [Commit the reviewed plan](../commit/)
- [Follow partition transfers](../../transfers/)
- [Inspect ring convergence](../../ring-status/)
- [Inspect member status](../../member-status/)

# Reviewed against

3.4.0: 961b3918247ac2f87369d14aa5c7da56b3feccdda2e5cb8951591e8606c112d7
3.4.1: 961b3918247ac2f87369d14aa5c7da56b3feccdda2e5cb8951591e8606c112d7

# Tags

feature: cluster-management
repository: riak_core
module: riak_core_console
concept: partition-placement
