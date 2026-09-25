# Description

Directories searched when Clique loads configuration schemas for the administrative CLI. If unset, the registry loads schemas from the Erlang library directory.

# Datatype

List

# Constraints

- List of directory path strings passed to the Clique schema loader.

# Inferred default

`[code:lib_dir()]`, determined by the running Erlang installation.

# Tags

feature: cluster-management
repository: riak_core
module: riak_core_cli_registry
concept: filesystem-layout

# Notes

This is the Erlang application environment key `schema_dirs` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_cli_registry.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_cli_registry.erl#L49)

# Reviewed against

3.4.0: bc59adf69fc9b469cb950c54b12a6a61307912a976b744f7d59e2ec7ca261614
3.4.1: bc59adf69fc9b469cb950c54b12a6a61307912a976b744f7d59e2ec7ca261614
