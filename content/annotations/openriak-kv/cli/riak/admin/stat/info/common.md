# Metadata

command: shell:riak admin stat info
versions: 3.4.0, 3.4.1

# Summary

Inspect metadata of matching metrics.

# Description

The handler expects attribute flags and the metric selector in one string. The packaged launcher splits that string again, so selecting multiple attributes currently fails even when quoted. Use a single metric selector to read all attributes. From `riak attach`, the equivalent direct call is `riak_core_console:stat_info(["-name -type riak.riak_kv.node.gets"]).`

Selectors can match multiple metrics. Use a specific selector when changing collection state or resetting counters. A metric’s supported datapoints depend on its type.

# Arguments

## entry

datatype: metric selector
required: true
repeatable: false

### Description

Metric name or pattern. For example, `cli_reference.requests`; suffixes can filter type/status or choose datapoints, such as `/status=enabled` or `/value`. Quote wildcard patterns so the shell does not expand them.

# Options

## -cache

datatype: flag (no value)
required: false
repeatable: true

### Description

Include the metric’s cache attribute in the information output.

## -datapoints

omit: true

datatype: flag (no value)
required: false
repeatable: true

### Description

Include the metric’s datapoints attribute in the information output.

## -module

datatype: flag (no value)
required: false
repeatable: true

### Description

Include the metric’s module attribute in the information output.

## -name

datatype: flag (no value)
required: false
repeatable: true

### Description

Include the metric’s name attribute in the information output.

## -options

datatype: flag (no value)
required: false
repeatable: true

### Description

Include the metric’s options attribute in the information output.

## -ref

omit: true

datatype: flag (no value)
required: false
repeatable: true

### Description

Include the metric’s ref attribute in the information output.

## -status

datatype: flag (no value)
required: false
repeatable: true

### Description

Include the metric’s status attribute in the information output.

## -timestamp

datatype: flag (no value)
required: false
repeatable: true

### Description

Include the metric’s timestamp attribute in the information output.

## -type

datatype: flag (no value)
required: false
repeatable: true

### Description

Include the metric’s type attribute in the information output.

## -value

datatype: flag (no value)
required: false
repeatable: true

### Description

Include the metric’s value attribute in the information output.

# Errors

## reference-error-1

### Condition

The selector contains an unknown status, type or datapoint.

### Description

Selector parsing or metric lookup can fail, or the selection can be empty.

### Remedy

Use info to inspect metric names/types; use enabled, disabled or * as a status filter and select a datapoint supported by the metric type.

# Examples

## shell-riak-admin-stat-info:a-diagnostic-counter

### Description

Inspect a counter’s attributes before changing it. This example counter starts at seven.

# Reviewed against

3.4.0: bb54e59c464eb6c746354d00d374c7e954128b8cc00ae67adda951df18418492
3.4.1: bb54e59c464eb6c746354d00d374c7e954128b8cc00ae67adda951df18418492

# Tags

feature: observability
repository: riak_core
module: riak_core_console
concept: diagnostics
