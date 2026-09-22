# Metadata

command: shell:riak admin handoff
versions: 3.4.0, 3.4.1

# Summary

Inspect and control partition transfers.

# Description

Read summary or details to inspect transfers. Use config to inspect limits and enable or disable to control directions.

# Arguments

# Examples

## reference-example-1

title: Choose a subcommand

### Invocation

```sh
riak admin handoff
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

3.4.0: e47c2c3cb2605c361b42ca8bf7f40dfd9409f08f1aff04864012ff18576fc7cf
3.4.1: e47c2c3cb2605c361b42ca8bf7f40dfd9409f08f1aff04864012ff18576fc7cf
