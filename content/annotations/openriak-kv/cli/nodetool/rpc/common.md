# Metadata

command: shell:nodetool rpc
versions: 3.4.0, 3.4.1

# Summary

Run a release-helper operation over Erlang distribution.

# Description

This bundled helper is normally invoked by the Riak launcher. Prefer riak ping, rpc or eval, which supply the configured target and cookie.

# Arguments

## Module

datatype: atom
required: true
repeatable: false

### Description

Exported function’s module.

## Function

datatype: atom
required: true
repeatable: false

### Description

Function to call.

## Arguments

datatype: Erlang terms
required: false
repeatable: true

### Description

Erlang terms passed to the function.

# Options

## -name

datatype: long node name
required: false
repeatable: false

### Description

Target full Erlang node name. Use this or -sname according to the node’s distribution mode.

## -sname

datatype: short node name
required: false
repeatable: false

### Description

Target short Erlang node name. Do not combine with -name.

## -setcookie

datatype: cookie text
required: false
repeatable: false

### Description

Distribution cookie matching the target node. Prefer the launcher so this is read from configuration.

## -start_epmd

datatype: boolean
required: false
repeatable: false

### Description

Whether the helper may start epmd.

# Examples

## reference-example-1

title: Use the launcher

### Invocation

```sh
riak rpc erlang node
```

### Description

The launcher supplies the helper’s distribution flags.

### Expected output

pong for ping, or the evaluated Erlang result for rpc/eval.

# Errors

## reference-error-1

### Condition

The target cannot be reached or the remote function fails.

### Description

The helper reports a node-connectivity or RPC error.

### Remedy

Check node-name mode, cookie, connectivity and the called function’s arguments.

# Results

## reference-result-1

### Description

Prints the remote result or a distribution/RPC failure.

# Reviewed against

3.4.0: 8dd23c5259e02896351604cd6a1a0e01e92d2b4f29a3ebe7e6559bbda325e6a6
3.4.1: 8dd23c5259e02896351604cd6a1a0e01e92d2b4f29a3ebe7e6559bbda325e6a6

# Tags

feature: node-operations
repository: riak
module: nodetool
concept: node-lifecycle
