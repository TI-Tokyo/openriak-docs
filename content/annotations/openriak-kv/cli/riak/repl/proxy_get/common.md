# Metadata

command: shell:riak repl proxy_get
versions: 3.4.0, 3.4.1

# Summary

Configure Riak CS proxy GET destinations.

# Description

Enable or disable remote block providers for Riak CS. This does not configure normal KV reads.

# Arguments

# Examples

## reference-example-1

title: Choose a subcommand

### Invocation

```sh
riak repl proxy_get
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

3.4.0: 905936b9a463534672e4de0c98854c993ad126d8345a0c58e0f6169bac5ed171
3.4.1: 905936b9a463534672e4de0c98854c993ad126d8345a0c58e0f6169bac5ed171
