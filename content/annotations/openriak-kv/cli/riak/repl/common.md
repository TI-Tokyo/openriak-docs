# Metadata

command: shell:riak repl
versions: 3.4.0, 3.4.1

# Summary

Manage cluster replication and inspect its state.

# Description

Name the local cluster, establish control connections, then configure realtime or full-sync destinations. Legacy listener/site subcommands remain for older deployments.

# Arguments

# Examples

## reference-example-1

title: Choose a subcommand

### Invocation

```sh
riak repl
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

# Results

## reference-result-1

### Description

The selected subcommand determines the result. Invoking the group without a valid subcommand displays usage rather than performing a data operation.

# Options

## -port

omit: true



## -block-provider-redirect

omit: true

# Reviewed against

3.4.0: 156f685c917e0cb7e06ad4965d079e2cc091ff85d949a95bf8245ac0f54e7b27
3.4.1: 156f685c917e0cb7e06ad4965d079e2cc091ff85d949a95bf8245ac0f54e7b27

# Tags

feature: legacy-replication
repository: riak
module: riak-repl
concept: cross-cluster-replication
