# Metadata

command: shell:riak remote_console
versions: 3.4.0, 3.4.1

# Summary

Open a remote Erlang shell on the configured node.

# Description

Starts a separate shell VM and connects over Erlang distribution. The node name and cookie must match; use this when a run_erl pipe is unavailable.

# Arguments

# Examples

## reference-example-1

title: Service-account invocation

### Invocation

```sh
riak remote_console
```

### Description

Run as the account that owns the node. For startup commands, first ensure the node is stopped; replace VERSION with the installed release directory where shown.

### Expected output

A shell prompt connected to the configured running node.

# Results

## reference-result-1

### Description

A shell prompt connected to the configured running node.

# Reviewed against

3.4.0: 870df629a0764230ca4d6fdcb9eaa815a8ade547a60a26f8208a435c44a544ea
3.4.1: 870df629a0764230ca4d6fdcb9eaa815a8ade547a60a26f8208a435c44a544ea

# Tags

feature: node-operations
repository: riak
module: riak
concept: node-lifecycle
