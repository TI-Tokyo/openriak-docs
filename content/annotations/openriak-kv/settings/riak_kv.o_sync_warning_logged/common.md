# Description

Internal marker that prevents repeated logging of the Bitcask `o_sync` compatibility warning on Linux. The backend sets it after logging; it does not change disk synchronization behaviour.

# Datatype

Runtime flag

# Constraints

- The writer stores `true`. Presence of any value suppresses the warning, so setting `false` does not reset it; remove the key to reset.

# Inferred default

Unset until the warning is emitted, then `true`.

# Tags

feature: bitcask
repository: riak_kv
module: riak_kv_bitcask_backend
concept: diagnostics, runtime

# Notes

This is the Erlang application environment key `o_sync_warning_logged` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_bitcask_backend.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_bitcask_backend.erl#L534)

# Reviewed against

3.4.0: 1c5d15266003bc0f80061f921de9b52d30085d32df27834ee5eda638b7e1cec8
3.4.1: 27087c3495fd70f622208a0c8d49c982b8a8a929c01ccfeced5cd9b414bd5ead
