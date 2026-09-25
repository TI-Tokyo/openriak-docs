# Description

Directory for per-partition vnode status files, which persist vnode identity and counter state. The fallback is `kv_vnode` beneath the platform data directory.

# Datatype

Directory path

# Constraints

- Writable directory path string for vnode status files.

# Inferred default

`filename:join(DataDir, "kv_vnode")`, using the status manager's supplied data directory or `riak_core.platform_data_dir` (whose application default is `"data"`).

# Tags

feature: object-storage
repository: riak_kv
module: riak_kv_vnode_status_mgr
concept: filesystem-layout, storage

# Notes

This is the Erlang application environment key `vnode_status` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_vnode_status_mgr.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_vnode_status_mgr.erl#L341)

Additional type/default evidence:

- [riak_core/src/riak_core.app.src](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core.app.src)

# Reviewed against

3.4.0: 10843df42309573da7e2399370a45e9b7f1752850710c591828a57c1114875ef
3.4.1: 94000a747fb8c2fa1f6984778f79f6c5763f795913c2b7adecb82dca4155a71e
