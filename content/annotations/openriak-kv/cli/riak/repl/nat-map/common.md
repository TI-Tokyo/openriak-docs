# Metadata

command: shell:riak repl nat-map
versions: 3.4.0, 3.4.1

# Summary

Manage address translations for replication peers.

# Description

List, add or delete mappings between external advertised addresses and internal reachable addresses.

# Arguments

# Examples

## reference-example-1

title: Choose a subcommand

### Invocation

```sh
riak repl nat-map
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

3.4.0: 42869951cedd825b0deb12da24cf21158725f937df1b6a634b00ff145eba5d19
3.4.1: 42869951cedd825b0deb12da24cf21158725f937df1b6a634b00ff145eba5d19
