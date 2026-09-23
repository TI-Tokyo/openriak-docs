# Description

Interval in milliseconds between checks for a due Tictac tree rebuild. A longer interval can reduce competing rebuild activity while a long-absent node is reintroduced and handoffs are running.

# Tags

feature: tictac-aae
repository: riak_kv
module: riak_kv_vnode
concept: replica-repair, scheduling

# Reviewed against

3.4.0: 20474ea6be580d0d812dec1671ca0fb86ace061b2e6fde36fed33dd2ebb112fa
3.4.1: 3b1039579270e798a68dc13415d08f6ddcddc75a3e8a104298408a22b05bee0b
