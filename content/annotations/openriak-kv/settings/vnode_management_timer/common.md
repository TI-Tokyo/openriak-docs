# Description

Interval between vnode-manager activities, including attempts to prompt handoff. Shorter intervals revisit pending work sooner; transfer limits and subsystem deferrals still control whether handoffs can start.

# Tags

feature: handoff
repository: riak_core
module: riak_core_vnode_manager
concept: partition-transfer

# Reviewed against

3.4.0: 1b5ec8c64ebd211f9e4e42d9ffea256d804cca3fcc0380f7cdaa15c6e76e1900
3.4.1: 4635e611f933ec217600214fbc6f9551304495e432a004a22e77ebd6833d09ee
