# Metadata

command: shell:riak admin stat
versions: 3.4.0, 3.4.1

# Summary

Inspect and manage individual metrics.

# Description

Select statistics by metric name or pattern. Use info to inspect metadata and show for values; enabling, disabling and resetting change metric collection or counters.

# Arguments

# Examples

## reference-example-1

title: Choose a subcommand

### Invocation

```sh
riak admin stat
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

3.4.0: f4bfa39b6275e97f5005cbf98af35e71cd1ecebd697c8489fb05bbd037e8790f
3.4.1: f4bfa39b6275e97f5005cbf98af35e71cd1ecebd697c8489fb05bbd037e8790f
