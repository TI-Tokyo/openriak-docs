# Metadata

command: shell:riak restart
versions: 3.4.0, 3.4.1

# Summary

Restart Erlang applications without replacing the VM process.

# Description

Invokes init:restart/0 on the running node. Application availability is interrupted while the runtime restarts.

# Arguments

# Examples

## reference-example-1

title: Service-account invocation

### Invocation

```sh
riak restart
```

### Description

Run as the account that owns the node. For startup commands, first ensure the node is stopped; replace VERSION with the installed release directory where shown.

### Expected output

The RPC is submitted; the node becomes unavailable temporarily while restarting.

# Results

## reference-result-1

### Description

The RPC is submitted; the node becomes unavailable temporarily while restarting.

# Reviewed against

3.4.0: 4a72d2a01d6c11a44c75411475729348a47138e46c4acbfa8280e623e0ec5ad1
3.4.1: 4a72d2a01d6c11a44c75411475729348a47138e46c4acbfa8280e623e0ec5ad1

# Tags

feature: node-operations
repository: riak
module: riak
concept: node-lifecycle
