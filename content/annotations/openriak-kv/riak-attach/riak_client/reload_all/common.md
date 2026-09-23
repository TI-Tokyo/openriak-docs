# Metadata

command: erlang:riak_client:reload_all/2
versions: 3.4.0, 3.4.1

# Summary

Reload a module on all ring members.

# Description

The module must be available on every target node’s code path. Review per-node results before relying on the new code.

# Arguments

## Module

datatype: Erlang module atom
required: true
repeatable: false

### Description

Module atom, for example `riak_client`.

## Client

datatype: riak_client handle
required: true
repeatable: false

### Description

See the shared `Client` argument on the parent module page.

# Reviewed against

3.4.0: 02bf087784609245b8d88fbe8e267fcf5218fa83ac6ca5450ac201f9079ad354
3.4.1: 02bf087784609245b8d88fbe8e267fcf5218fa83ac6ca5450ac201f9079ad354

# Tags

feature: client-operations
repository: riak_kv
module: riak_client
concept: data-access
