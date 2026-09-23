# Description

Maximum number of times a secondary subsystem can defer a vnode's handoff. The delay is approximately this count multiplied by `vnode_management_timer`; zero prevents those subsystem deferrals.

# Tags

feature: handoff
repository: riak_kv
module: riak_kv_vnode
concept: partition-transfer

# Reviewed against

3.4.0: 137d284fab8139a0c1ac26f2142390b553d94ba7d7b145148e6454d645bbe228
3.4.1: 3f01c87d3a08ff7b0cbb54821851bb22bc76b9e868d4cc93eb7ea41505c160c6
