# Description

Controls whether the node watcher installs periodic health checks when a service registers a health-check callback. Disabling it skips those checks while retaining the service registration.

# Datatype

Boolean

# Allowed values

- `true`
- `false`

# Constraints

- Use the Erlang atoms `true` or `false`.

# Inferred default

`true`.

# Tags

feature: cluster-management
repository: riak_core
module: riak_core_node_watcher
concept: diagnostics

# Notes

This is the Erlang application environment key `enable_health_checks` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_node_watcher.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_node_watcher.erl#L208)

# Reviewed against

3.4.0: d00ab43555e1dc7f80fd1e536e9ca5de6178ea970ff0c1ced7718ed96cf5b78f
3.4.1: d00ab43555e1dc7f80fd1e536e9ca5de6178ea970ff0c1ced7718ed96cf5b78f
