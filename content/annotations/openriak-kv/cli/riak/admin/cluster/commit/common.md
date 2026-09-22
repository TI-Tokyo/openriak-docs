# Metadata

command: shell:riak admin cluster commit
versions: 3.4.0, 3.4.1

# Summary

Apply the cluster changes shown by the last reviewed plan.

# Description

Run commit after reviewing cluster plan. It accepts the reviewed changes and starts asynchronous partition movement. If a node joins or another staged action changes after planning, refresh and review the plan before retrying.

# Arguments

# Notes

The examples expand node1 into a five-node cluster. They first add node2, then add nodes3 through node5.

| Situation | Expected commit result |
| --- | --- |
| No joins and no plan | Refused: verify a plan first |
| No joins, after an empty plan | Refused: there is no reviewed change set |
| One staged join, without plan | Refused: verify that join’s plan |
| One staged join, after plan | Changes committed; transfers begin |
| Another node joins after plan | Refused: the plan has changed |
| The complete five-node plan has been reviewed | Changes committed; wait for convergence |
| The same plan was already committed | Refused: the reviewed plan has been consumed |

The command can print a refusal and still exit with status `0`. Read the result text; an exit status alone does not establish that any changes were committed.

# Results

## outcome

### Description

`Cluster changes committed` means the reviewed change set was accepted. Wait for handoffs and ring convergence before considering the expansion complete.

# Related documentation

- [Review the cluster plan](../plan/)
- [Stage a join](../join/)
- [Follow partition transfers](../../transfers/)
- [Inspect ring convergence](../../ring-status/)
- [Inspect member status](../../member-status/)

# Reviewed against

3.4.0: fe8b47ff15832f90147ba428819dd534cb57b54d7894fd117a09f32cda053943
3.4.1: fe8b47ff15832f90147ba428819dd534cb57b54d7894fd117a09f32cda053943
