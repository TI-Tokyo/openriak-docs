# Metadata

command: erlang:riak:stop/0
versions: 3.4.0, 3.4.1

# Summary

Stop the Riak node from an Erlang shell.

# Description

Requests VM shutdown with init:stop/0. This stops the node, not merely the attached shell. Use the operating-system service manager when it owns the process.

# Arguments

## Reason

datatype: Erlang term
required: false
repeatable: false

### Description

Optional reason written to the node log. The zero-argument form supplies a default stop message.

# Examples

## reference-example-1

title: Planned shutdown

### Invocation

```erlang
riak:stop("planned maintenance").
```

### Description

Run only as part of a planned node shutdown. To leave an attached shell without stopping Riak, detach instead.

### Expected output

The reason is logged and the VM shuts down; the shell connection is lost.

# Errors

## reference-error-1

### Condition

The external service manager restarts the VM after shutdown.

### Description

The node returns even though this function requested a stop.

### Remedy

Stop or pause the owning service manager for an intentional maintenance outage.

# Results

## reference-result-1

### Description

The VM terminates. An external supervisor may restart it unless the service is stopped through that supervisor.

# Reviewed against

3.4.0: 44590d9bee9f1f44f88f355a962d8c100c015317fbd4048268a430329986b923
3.4.1: 44590d9bee9f1f44f88f355a962d8c100c015317fbd4048268a430329986b923

# Tags

feature: node-operations
repository: riak_kv
module: riak
concept: node-lifecycle
