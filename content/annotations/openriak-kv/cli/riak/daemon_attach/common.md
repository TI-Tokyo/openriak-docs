# Metadata

command: shell:riak daemon_attach
versions: 3.4.0, 3.4.1

# Summary

Attach a terminal to a daemon’s Erlang shell.

# Description

Connects through the run_erl pipe directory. The account needs write access to that directory. Detach without stopping the node.

# Arguments

# Examples

## reference-example-1

title: Service-account invocation

### Invocation

```sh
riak daemon_attach
```

### Description

Run as the account that owns the node. For startup commands, first ensure the node is stopped; replace VERSION with the installed release directory where shown.

### Expected output

An interactive Erlang shell on the running daemon.

# Errors

## reference-error-1

### Condition

The pipe directory is not writable by the invoking account.

### Description

The launcher reports insufficient privileges and does not attach.

### Remedy

Use the node’s service account and the correct pipe directory.

# Results

## reference-result-1

### Description

An interactive Erlang shell on the running daemon.

# Reviewed against

3.4.0: f0c8a0562f88c59257676afe64c867a2afb7ca84ba492d79cc2af490ea2c400e
3.4.1: f0c8a0562f88c59257676afe64c867a2afb7ca84ba492d79cc2af490ea2c400e
