# Metadata

command: shell:riak stop
versions: 3.4.0, 3.4.1

# Summary

Stop the running node and wait for it to exit.

# Description

Runs shutdown hooks, requests init:stop/0, then waits for the process and distribution endpoint to disappear. If an external supervisor owns the process, stop it through that supervisor.

# Arguments

# Examples

## reference-example-1

title: Service-account invocation

### Invocation

```sh
riak stop
```

### Description

Run as the account that owns the node. For startup commands, first ensure the node is stopped; replace VERSION with the installed release directory where shown.

### Expected output

The VM exits; the launcher returns after shutdown checks.

# Results

## reference-result-1

### Description

The VM exits; the launcher returns after shutdown checks.

# Reviewed against

3.4.0: a6d971d37f326a94d8c90cfad49008042ceca6e345cbbac7f4b6ba6c5dfd4341
3.4.1: a6d971d37f326a94d8c90cfad49008042ceca6e345cbbac7f4b6ba6c5dfd4341

# Tags

feature: node-operations
repository: riak
module: riak
concept: node-lifecycle
