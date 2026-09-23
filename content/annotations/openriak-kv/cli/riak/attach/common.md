# Metadata

command: shell:riak attach
versions: 3.4.0, 3.4.1

# Summary

Attach an interactive Erlang shell to the running node.

# Description

Use this shell for administrative Erlang expressions. End each expression with a period. Detach from the shell without calling q/0 or init:stop/0, which stop the node.

# Notes

The attached shell executes with the node’s privileges. Use the documented function pages for argument types and effects.

# Arguments

# Examples

## reference-example-1

title: Open the shell

### Invocation

```sh
riak attach
```

### Description

Open an attached shell, then evaluate `node().` to check which node you reached.

### Expected output

An Erlang shell prompt; node(). returns the node name.

# Errors

## reference-error-1

### Condition

A function or arity is absent in this release.

### Description

The shell raises `undef`.

### Remedy

Check the selected version and the function’s module and arity.

## reference-error-2

### Condition

An argument does not match a function clause or guard.

### Description

The shell can raise `function_clause` or `badarg`.

### Remedy

Use the documented Erlang types, tuple shapes and supported values.

## reference-error-3

### Condition

The server process required by an administrative function is not running.

### Description

A synchronous gen_server call can exit with `noproc`; an unresponsive process can cause a timeout.

### Remedy

Check application startup and node logs. Do not treat an asynchronous cast acknowledgment as confirmation that work completed.

# Results

## reference-result-1

### Description

An interactive shell connected to the running Erlang VM. Function expressions print Erlang return terms rather than shell exit codes.

# Reviewed against

3.4.0: 5575ad9cd8c1d4cf05b4ed42daeeff1c53216d2fb1c0e9e01cc31c8f9f60e58a
3.4.1: 5575ad9cd8c1d4cf05b4ed42daeeff1c53216d2fb1c0e9e01cc31c8f9f60e58a

# Tags

feature: node-operations
repository: riak
module: riak
concept: node-lifecycle
