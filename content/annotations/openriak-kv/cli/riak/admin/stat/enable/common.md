# Metadata

command: shell:riak admin stat enable
versions: 3.4.0, 3.4.1

# Summary

Enable matching metrics.

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

## shell-riak-admin-stat-enable:a-diagnostic-counter

### Description

Enable a counter so it can collect measurements. Expect an acknowledgement of the enabled state.

# Reviewed against

3.4.0: 4c9f24314817051c7748f2503b983e0567b92de50042aa83ab870704b2ee1b32
3.4.1: 4c9f24314817051c7748f2503b983e0567b92de50042aa83ab870704b2ee1b32
