# Metadata

command: shell:riak repl fullsync
versions: 3.4.0, 3.4.1

# Summary

Configure and control full-sync replication.

# Description

Enable a destination before starting a full comparison. Use status to inspect running comparisons and worker-limit subcommands to control concurrency.

# Arguments

# Examples

## reference-example-1

title: Choose a subcommand

### Invocation

```sh
riak repl fullsync
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

# Reviewed against

3.4.0: f95a12855e39cb4a9ce637d8299995cf8d65baeb3b017b4121c8f3237168f74f
3.4.1: f95a12855e39cb4a9ce637d8299995cf8d65baeb3b017b4121c8f3237168f74f

# Tags

feature: full-sync
repository: riak
module: riak-repl
concept: replica-repair
