# Description

Check vnode mailbox load before choosing a PUT coordinator. This avoids sending new work to an already congested vnode, but the checks can add latency; disabling it restores the older unchecked selection behaviour.

# Tags

feature: request-processing
repository: riak_kv
module: riak_kv_put_fsm
concept: overload-protection

# Reviewed against

3.4.0: 09bcb7400793c5448b53ae6d5ce0ea63010e175215dc02fdf54e79339da72ce0
3.4.1: 7327250c18abf1413545a51b194a32092f021986af329b0405d10536b7e40047
