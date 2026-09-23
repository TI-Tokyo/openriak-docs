# Description

Cluster-wide limit on handoffs prompted by scheduled vnode-manager activity. A node starts another prompted transfer only while the observed ongoing or blocked count is below this limit; `transfer_limit` also limits transfers at each node.

# Tags

feature: handoff
repository: riak_core
module: riak_core_vnode_manager
concept: partition-transfer

# Reviewed against

3.4.0: 8c99801b2bd42179b0a67ac64ab42e440cd01da1ce69e5289680fab54dff26fb
3.4.1: bae21c37c8671ec340ec5e7d1e294ef1664dd101c593531d8136ffba48837f97
