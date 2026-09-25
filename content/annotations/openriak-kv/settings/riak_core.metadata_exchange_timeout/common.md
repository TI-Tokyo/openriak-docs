# Description

Timeout, in milliseconds, passed to cluster metadata anti-entropy exchanges. It also bounds the wait when a caller explicitly attempts an exchange and waits for completion.

# Datatype

Timeout

# Units

- milliseconds

# Constraints

- Non-negative integer FSM timeout, or `infinity`.

# Inferred default

`60000`.

# Tags

feature: cluster-management
repository: riak_core
module: riak_core_metadata_manager
concept: replica-repair

# Notes

This is the Erlang application environment key `metadata_exchange_timeout` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_metadata_manager.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_metadata_manager.erl#L311)

# Reviewed against

3.4.0: 308ba66e3ba6fa35376e4399300d4eacedc7e8b180c402b27ad8675457b883ee
3.4.1: 308ba66e3ba6fa35376e4399300d4eacedc7e8b180c402b27ad8675457b883ee
