# Metadata

command: erlang:riak_client:resync_bucket/1
versions: 3.4.1

# Summary

Request a bucket resynchronisation using built-in defaults.

# Description

Uses the full-sync manager’s bucket-resync path. A usable destination must already be configured; this function does not choose a destination.

# Arguments

## Bucket

datatype: binary or pair of binaries
required: true
repeatable: false

### Description

See the shared `Bucket` argument on the parent module page.

# Examples

## reference-example-1

title: Resynchronise one bucket

### Invocation

```erlang
riak_client:resync_bucket(<<"cli_reference">>).
```

### Description

Run after configuring and checking the full-sync destination.

### Expected output

A resynchronisation request acknowledgment or a manager error.

# Errors

## reference-error-1

### Condition

The full-sync manager or destination is unavailable.

### Description

The request can fail or fail to make progress.

### Remedy

Inspect the manager configuration and destination connectivity before retrying.

# Results

## reference-result-1

### Description

The manager handles the requested resynchronisation; inspect replication progress to determine completion.

# Reviewed against

3.4.1: 038a90e2f38edaeb0a69a9c7754e6411d812916d8653f530773e7ca161d27caf
