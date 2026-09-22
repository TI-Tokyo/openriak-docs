# Metadata

command: shell:riak admin stat reset
versions: 3.4.0, 3.4.1

# Summary

Reset matching metric values.

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

## shell-riak-admin-stat-reset:a-diagnostic-counter

### Description

Reset a counter when starting a new measurement interval. Its value changes from seven to zero.

# Reviewed against

3.4.0: 134531f68528ee90b7bb7b158a5f8c05c6ea4f511e7b2aa65ee28c8506530121
3.4.1: 134531f68528ee90b7bb7b158a5f8c05c6ea4f511e7b2aa65ee28c8506530121
