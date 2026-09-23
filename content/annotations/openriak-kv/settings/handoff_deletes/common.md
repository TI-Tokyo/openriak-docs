# Description

Forward delete requests during handoff so tombstones can still be reaped when `delete_mode` is not `keep`. This concerns deletion propagation during transfers, not the general tombstone retention period.

# Tags

feature: handoff
repository: riak_kv
module: riak_kv_vnode
concept: partition-transfer

# Reviewed against

3.4.0: dde11b65dd90d5eec75bd71760b72a21235d7790a54e9b7bd01c30b0db3c3013
3.4.1: 0916bf6ce9cf650724e7d60cc063c27e5e44daf8bbb84d7f7c3262028fa0d700
