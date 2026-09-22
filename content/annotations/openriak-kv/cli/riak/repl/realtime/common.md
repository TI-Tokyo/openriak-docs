# Metadata

command: shell:riak repl realtime
versions: 3.4.0, 3.4.1

# Summary

Configure and control realtime replication.

# Description

Enable destinations, start or stop their streams, and choose a cascading policy. A configured destination still needs a working control connection.

# Arguments

# Examples

## reference-example-1

title: Choose a subcommand

### Invocation

```sh
riak repl realtime
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

3.4.0: 2b43639565c2581942b12374d87067ef791e9e8f5a4506e8ba69b9356a3a78ba
3.4.1: 2b43639565c2581942b12374d87067ef791e9e8f5a4506e8ba69b9356a3a78ba
