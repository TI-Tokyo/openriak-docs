# Metadata

command: shell:riak admin tictacaae
versions: 3.4.0, 3.4.1

# Summary

Inspect and control Tictac active anti-entropy.

# Description

Inspect tree status and runtime scheduling settings, request rebuilds, or query AAE data with fold. Data-removal selectors require careful range selection.

# Arguments

# Examples

## reference-example-1

title: Choose a subcommand

### Invocation

```sh
riak admin tictacaae
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

3.4.0: f784357630ae1e1d48327e1a70ef223b37a511c55650a57486a5cfef0312a75e
3.4.1: f784357630ae1e1d48327e1a70ef223b37a511c55650a57486a5cfef0312a75e
