# Metadata

command: shell:riak admin security
versions: 3.4.0, 3.4.1

# Summary

Manage users, groups, authentication sources and permissions.

# Description

Configure identities, source rules and grants before enabling security. Authentication sources identify clients; grants control access to data.

# Arguments

# Examples

## reference-example-1

title: Choose a subcommand

### Invocation

```sh
riak admin security
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

3.4.0: 1107ed6dd53d22a457b8100607118fc4d6d8b2682488cc9947072b601c67c83b
3.4.1: 1107ed6dd53d22a457b8100607118fc4d6d8b2682488cc9947072b601c67c83b
