# Description

Timeout, in milliseconds, for synchronous lock requests to the legacy entropy manager. It limits how long callers wait to obtain permission to perform anti-entropy work.

# Datatype

Timeout

# Units

- milliseconds

# Constraints

- Non-negative integer call timeout, or `infinity`.

# Inferred default

`10000`.

# Tags

feature: legacy-aae
repository: riak_kv
module: riak_kv_entropy_manager
concept: replica-repair

# Notes

This is the Erlang application environment key `anti_entropy_lock_timeout` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_entropy_manager.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_entropy_manager.erl#L98)

# Reviewed against

3.4.0: d5c70d7d435857f1b45ecfe1ea4aacb8a49e25ff6c3896cfb01380f6f3959e74
3.4.1: b85d3b3a0d0f7dcc3c22149fe913c7b122e79e6121a90926cd465f771885f969
