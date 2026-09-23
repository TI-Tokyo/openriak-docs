# Description

Defer fetching full objects during partition repair until their keys pass repair filters. Used with `repair_span = double_pair` and a backend supporting head folds, such as Leveled, to avoid reading objects another repair source will supply.

# Tags

feature: handoff
repository: riak_kv
module: riak_kv_vnode
concept: partition-transfer

# Reviewed against

3.4.0: efcf72b500e5b7bbb991e87f5474c62e9404fe37d398cea7ac27c1ea94e09eae
3.4.1: a1bd6e8ffbffb48cbec9b7f86e005671129200d6ff3b2815b242d2f97946d300
