# Metadata

command: shell:riak admin erl-reload
versions: 3.4.0, 3.4.1

# Summary

Reload Erlang modules from the node’s configured paths.

# Description

This is an administrative code-reload operation. Ensure the intended modules are installed consistently before invoking it.

# Arguments

# Examples

## shell-riak-admin-erl-reload:reload-installed-modules

### Description

Request module reload on the node.

# Reviewed against

3.4.0: e40c18c0b8adb423f6a5cd4f90a7f8577be7a1722eccd02d152fab0983fddbb2
3.4.1: e40c18c0b8adb423f6a5cd4f90a7f8577be7a1722eccd02d152fab0983fddbb2

# Tags

feature: node-operations
repository: riak_kv
module: riak_kv_console
concept: node-lifecycle
