# Metadata

command: shell:riak escript
versions: 3.4.0, 3.4.1

# Summary

Run an escript with the release’s Erlang environment.

# Description

The script has access to the release libraries. Supply its path and then any arguments expected by that script.

# Arguments

## script

datatype: filesystem path
required: true
repeatable: false

### Description

Path to the escript to run.

## arguments

datatype: text
required: false
repeatable: true

### Description

Arguments passed to the escript. Their meaning depends on that script.

# Examples

## reference-example-1

title: Run an administrative script

### Invocation

```sh
riak escript /path/to/check.escript
```

### Description

Replace the path with a reviewed escript that performs the intended check.

### Expected output

Output and exit status are determined by the script.

# Errors

## reference-error-1

### Condition

The script is absent, invalid or fails during execution.

### Description

The escript runtime reports a load, syntax or runtime error.

### Remedy

Check the script path, Erlang syntax and required release libraries.

# Results

## reference-result-1

### Description

The launcher returns success when the escript succeeds; otherwise it exits nonzero.

# Reviewed against

3.4.0: 97552f3b13fa169463b6dcd20ff18903e188ceebadec0fe51d185ac47a7a0ef5
3.4.1: 97552f3b13fa169463b6dcd20ff18903e188ceebadec0fe51d185ac47a7a0ef5

# Tags

feature: node-operations
repository: riak
module: riak
concept: node-lifecycle
