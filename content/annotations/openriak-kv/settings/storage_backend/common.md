# Description

Storage engine used for KV objects and, where supported, secondary indexes. Choose according to durability, memory and query requirements. Changing this setting does not convert existing data between backend formats.

# Tags

feature: storage-backends
repository: riak_kv
module: riak_kv_app, riak_kv_memory_backend, riak_kv_stat_bc, riak_kv_status, riak_kv_sup, riak_kv_vnode
concept: backend-selection, storage

# Reviewed against

3.4.0: 0927d6940f40f36984afea7a41540f7505400f6c851cd8bf19a0e3a85244368f
3.4.1: d6a002fac9973934406513be161a01d7d17f660603e61520a1b25870db83eece
