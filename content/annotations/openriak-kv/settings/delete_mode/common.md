# Description

Choose how long delete tombstones remain: `keep` retains them for explicit reaping, `immediate` removes them immediately, and a duration delays removal. Retaining tombstones allows deletes to reach replicas and connected clusters; early removal can allow older copies to reappear. Use a consistent policy across reconciling clusters.

# Tags

feature: deletion
repository: riak_kv
module: riak_kv_eraser, riak_kv_vnode
concept: retention, tombstones

# Reviewed against

3.4.0: 5cdf5aed28e72e70f2fc8d59c389dbe5a34f06543911c96f0b326af970947e99
3.4.1: 91b0e4b4b9655d6b3581d4daeae8422f255d0aa0c460ca43fa802103a3d72c36
