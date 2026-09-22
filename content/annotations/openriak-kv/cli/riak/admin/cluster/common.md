# Metadata

command: shell:riak admin cluster
versions: 3.4.0, 3.4.1

# Summary

Plan membership and ring changes, and inspect cluster state.

# Description

Stage changes, review the plan, then commit. Read status and ownership information before and after topology changes.

# Arguments

# Options

## --node

omit: true

# Examples

## reference-example-1

title: Choose a subcommand

### Invocation

```sh
riak admin cluster
```

### Description

Display the launcher or command-group usage. Some groups return a nonzero status when invoked without a subcommand.

### Expected output

Usage text listing available subcommands.

# Errors

## reference-error-1

### Condition

No recognised subcommand was supplied.

### Description

Usage is printed; legacy groups can also return an error term or a nonzero process status.

### Remedy

Select a subcommand from the syntax links and provide its required arguments.

## joining-node-cookie

### Condition

A joining node uses a different Erlang distribution cookie from the cluster.

### Description

The local CLI can reach its own node while the inter-node connection fails. The join reports that the destination is not reachable, and the candidate does not enter the staged membership. Plan cannot include that failed join; commit cannot apply it. This message is also possible for DNS, network or node-availability failures, so it does not identify a cookie mismatch by itself.

### Remedy

Check the full node name, DNS resolution, network connectivity and the configured distribution cookies. Correct the candidate’s configuration, retry the join, then review the complete plan before committing. A CLI using the wrong cookie for its own node fails earlier; see the shared administrative errors on the parent page.

# Results

## reference-result-1

### Description

The selected subcommand determines the result. Invoking the group without a valid subcommand displays usage rather than performing a data operation.

# Reviewed against

3.4.0: 6fb040aabd63bd213f86610f90b08c9ee869535ba978e4ca9f95b59193653c21
3.4.1: 6fb040aabd63bd213f86610f90b08c9ee869535ba978e4ca9f95b59193653c21
