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

3.4.0: d9cf18e274ead7515611cf54e2c96b848472a9c89c3df58c3e955feca7b3dd54
3.4.1: d9cf18e274ead7515611cf54e2c96b848472a9c89c3df58c3e955feca7b3dd54

# Tags

feature: node-operations
repository: riak_kv
module: riak_kv_console
concept: node-lifecycle
