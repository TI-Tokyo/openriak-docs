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

3.4.0: 82c319b6fb2cf28fd1808a3c429e3bf3d5fb7cb5be7e5f3e4a4fec2c26ed4f46
3.4.1: 82c319b6fb2cf28fd1808a3c429e3bf3d5fb7cb5be7e5f3e4a4fec2c26ed4f46

# Tags

feature: node-operations
repository: riak
module: riak
concept: node-lifecycle
