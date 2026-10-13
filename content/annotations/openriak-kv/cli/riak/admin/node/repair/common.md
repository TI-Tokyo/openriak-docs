# Metadata

command: shell:riak admin node repair
versions: 3.4.1

# Summary

Start, inspect or stop partition repair.

# Description

Repair work runs asynchronously. Use status to follow progress and stop with a reason when cancellation is needed.

# Arguments

# Examples

## reference-example-1

title: Choose a subcommand

### Invocation

```sh
riak admin node repair
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

3.4.1: 6399ed01ea3fce46ed8b9e0a707b2d36a69a30b1595e4dadf0a921f13c896c8e

# Tags

feature: read-repair
repository: riak
module: riak
concept: replica-repair
