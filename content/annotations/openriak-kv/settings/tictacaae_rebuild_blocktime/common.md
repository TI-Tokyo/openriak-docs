# Description

Maximum vnode-blocking time in milliseconds while taking a tree-rebuild snapshot. The block is released after this bound even if snapshot completion is delayed, favouring vnode availability over eliminating every snapshot race.

# Tags

feature: tictac-aae
repository: riak_kv
module: riak_kv_vnode
concept: replica-repair

# Reviewed against

3.4.0: 0d75e291d2ecb297b8bec7435a65092170b13f4b4176e61bbc297c8a335c0fcc
3.4.1: d5f31d3ca073cb3a246ce1b1cb89e6278990238659a05740eda907f147134682
