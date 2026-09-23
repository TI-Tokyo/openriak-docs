# Metadata

command: shell:riak admin bucket-type
versions: 3.4.0, 3.4.1

# Summary

Manage bucket-type definitions and activation.

# Description

Create a type, inspect its properties, then activate it before writing to typed buckets. Use update for supported property changes.

# Arguments

# Examples

## reference-example-1

title: Choose a subcommand

### Invocation

```sh
riak admin bucket-type
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

3.4.0: 7aba1bdfc8aaa637083ff1e5c1df19e31ba9ee42aa2756be28da4e8e2a8f4801
3.4.1: 7aba1bdfc8aaa637083ff1e5c1df19e31ba9ee42aa2756be28da4e8e2a8f4801

# Tags

feature: bucket-properties
repository: riak
module: riak-admin
concept: data-policy
