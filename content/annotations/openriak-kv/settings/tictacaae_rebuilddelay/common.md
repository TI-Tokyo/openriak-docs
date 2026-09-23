# Description

Maximum randomized delay, in seconds, added when scheduling a Tictac tree rebuild. It spreads rebuilds across vnodes instead of making all eligible vnodes rebuild simultaneously.

# Tags

feature: tictac-aae
repository: riak_kv
module: riak_kv_vnode
concept: replica-repair, scheduling

# Reviewed against

3.4.0: 6d7fd8864cced65d642fd6848bc54e866a68e2ff42e1237c8f004f932b254cf6
3.4.1: 9046809c3b5121f66fbb324493ed0ac21ca348e392870e75950cb9a984735fdd
