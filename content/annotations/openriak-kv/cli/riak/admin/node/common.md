# Metadata

command: shell:riak admin node
versions: 3.4.1

# Summary

Manage node-level partition repair.

# Description

Use node repair to start repairs, inspect progress or cancel work.

# Arguments

# Examples

## reference-example-1

title: Choose a subcommand

### Invocation

```sh
riak admin node
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

3.4.1: 0335deabfbe36a97c5b3211e0387f156f3f03442caef2bfc77ef6cfac8bc3f4d

# Tags

feature: node-operations
repository: riak
module: riak-admin
concept: node-lifecycle
