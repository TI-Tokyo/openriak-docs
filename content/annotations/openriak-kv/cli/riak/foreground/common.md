# Metadata

command: shell:riak foreground
versions: 3.4.0, 3.4.1

# Summary

Start the node in the foreground without an interactive shell.

# Description

Intended for supervision by the operating-system service manager or a container runtime. The process remains attached to the invoking session.

# Arguments

# Examples

## reference-example-1

title: Service-account invocation

### Invocation

```sh
riak foreground
```

### Description

Run as the account that owns the node. For startup commands, first ensure the node is stopped; replace VERSION with the installed release directory where shown.

### Expected output

Application startup logs; the command remains running until the node stops.

# Errors

## reference-error-1

### Condition

Another VM uses the configured node name, or required runtime paths are not writable.

### Description

Startup fails with a distribution, boot-file, configuration or filesystem error.

### Remedy

Check the existing process and run as the service account; correct the boot/configuration paths and inspect the node logs.

# Results

## reference-result-1

### Description

Application startup logs; the command remains running until the node stops.

# Reviewed against

3.4.0: 0cf2a573318ba1584399302aa50fc9de61864747d63c71a65f9968d3905bb7c2
3.4.1: 0cf2a573318ba1584399302aa50fc9de61864747d63c71a65f9968d3905bb7c2

# Tags

feature: node-operations
repository: riak
module: riak
concept: node-lifecycle
