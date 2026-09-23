# Metadata

command: shell:riak admin downgrade-objects
versions: 3.4.0, 3.4.1

# Summary

Convert stored objects for compatibility with an older object format.

# Description

This is a maintenance operation that scans stored objects. Run it only as part of a version-specific downgrade procedure.

# Arguments

## kill-handoffs

datatype: boolean
required: true
repeatable: false

### Valid values

- true
- false

### Description

Whether active handoffs should be killed before conversion.

## concurrency

datatype: positive integer
required: false
repeatable: false

### Description

Number of concurrent conversion workers.

# Examples

## reference-example-1

title: Controlled conversion

### Invocation

```sh
riak admin downgrade-objects false 1
```

### Description

Perform only when required by a validated downgrade procedure. This example selects one worker and does not request handoff cancellation.

### Expected output

Conversion startup/progress, or a backend/compatibility error.

# Results

## reference-result-1

### Description

The conversion is a background maintenance job; monitor its completion before proceeding with a downgrade.

# Reviewed against

3.4.0: 8c4270541f49f90f229fc1128c1b393ec6e7ebc6318f9dff598543f9bd7b847e
3.4.1: 8c4270541f49f90f229fc1128c1b393ec6e7ebc6318f9dff598543f9bd7b847e

# Tags

feature: node-operations
repository: riak_kv
module: riak_kv_console
concept: node-lifecycle
