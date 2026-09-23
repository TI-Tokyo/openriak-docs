# Metadata

command: shell:riak rpc
versions: 3.4.0, 3.4.1

# Summary

Call an exported Erlang function on the running node.

# Description

Supply a module, function and Erlang argument terms. Use eval for expressions with local bindings or multiple steps.

# Arguments

## Mod

datatype: Erlang atom
required: true
repeatable: false

### Description

Exported function’s module, for example `erlang`.

## Fun

datatype: Erlang atom
required: true
repeatable: false

### Description

Function name, for example `node`.

## Args

datatype: Erlang terms
required: false
repeatable: true

### Description

Arguments as Erlang terms. Quote shell-sensitive terms. Omit for an arity-zero function.

# Reviewed against

3.4.0: f334c9bc5f552102ad170e5c314393049cb4064466ad28e9fcc8a3ce090bbe8d
3.4.1: f334c9bc5f552102ad170e5c314393049cb4064466ad28e9fcc8a3ce090bbe8d

# Tags

feature: node-operations
repository: riak
module: riak
concept: node-lifecycle
