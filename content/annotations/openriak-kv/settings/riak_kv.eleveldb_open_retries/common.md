# Description

Maximum number of attempts to open a LevelDB backend database when its lock is still held, for example during cleanup after a vnode crash. The implementation always makes at least one attempt and retries only lock-related open errors.

# Datatype

Integer

# Units

- attempts

# Constraints

- Integer attempt count; the consumer clamps it to at least `1`.

# Inferred default

`30`.

# Tags

feature: leveldb
repository: riak_kv
module: riak_kv_eleveldb_backend
concept: storage

# Notes

This is the Erlang application environment key `eleveldb_open_retries` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_eleveldb_backend.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_eleveldb_backend.erl#L690)

# Reviewed against

3.4.0: fdf4530cebbf8a0f2896e61d934b5f23496df3a93e5af02433807bd860b58e81
3.4.1: a4b915ebef7d4c0c49d9b908024ce2af5130b8a14501bb5c1ac8869cbb69af11
