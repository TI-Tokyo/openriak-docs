# Metadata

command: shell:riak admin stat show
versions: 3.4.0, 3.4.1

# Summary

Read values of matching metrics.

# Description

Selectors can match multiple metrics. Use a specific selector when changing collection state or resetting counters. A metric’s supported datapoints depend on its type.

# Arguments

## entry

datatype: metric selector
required: true
repeatable: false

### Description

Metric name or pattern. For example, `cli_reference.requests`; suffixes can filter type/status or choose datapoints, such as `/status=enabled` or `/value`. Quote wildcard patterns so the shell does not expand them.

# Errors

## reference-error-1

### Condition

The selector contains an unknown status, type or datapoint.

### Description

Selector parsing or metric lookup can fail, or the selection can be empty.

### Remedy

Use info to inspect metric names/types; use enabled, disabled or * as a status filter and select a datapoint supported by the metric type.

# Examples

## shell-riak-admin-stat-show:a-diagnostic-counter

### Description

Read a counter to inspect its current value. This example counter contains seven.

# Reviewed against

3.4.0: 2c577c11c1b3289532c4d2c7a59d32874d014fca119a2d93ebb4ded704dfa1e6
3.4.1: 2c577c11c1b3289532c4d2c7a59d32874d014fca119a2d93ebb4ded704dfa1e6
