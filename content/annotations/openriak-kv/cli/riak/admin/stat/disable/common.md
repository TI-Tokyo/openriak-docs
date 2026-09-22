# Metadata

command: shell:riak admin stat disable
versions: 3.4.0, 3.4.1

# Summary

Disable matching metrics.

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

## shell-riak-admin-stat-disable:a-diagnostic-counter

### Description

Disable a counter to stop collecting measurements. The example counter starts at seven.

# Reviewed against

3.4.0: 1ab9bc8a6cc98592e8dd7a6cb04ca7ef1f95a4a36cc6bc740e413b2371b5a8f5
3.4.1: 1ab9bc8a6cc98592e8dd7a6cb04ca7ef1f95a4a36cc6bc740e413b2371b5a8f5
