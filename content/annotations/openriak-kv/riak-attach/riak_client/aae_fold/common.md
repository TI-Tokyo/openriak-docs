# Metadata

command: erlang:riak_client:aae_fold/1
versions: 3.4.0, 3.4.1

# Summary

Run a cluster-wide query over active anti-entropy data.

# Description

Choose a query selector below. Cached-tree queries compare hashes; range queries scan AAE data and can inspect, replicate, repair or remove matching objects.

# Arguments

## Query

datatype: AAE query tuple
required: true
repeatable: false

### Description

Query tuple whose first element selects the operation, for example `{list_buckets, 3}`. Each selector page documents its tuple fields.

## Client

datatype: riak_client handle
required: false
repeatable: false

### Description

See the shared `Client` argument on the parent module page.

# Errors

## reference-error-1

### Condition

The query exceeds its coverage timeout.

### Description

Returns `{error, timeout}` or a worker error term.

### Remedy

Check AAE readiness and node health; reduce the query range when possible.

# Shared arguments

## KeyRange

datatype: all or binary key bounds

### Description

Key range inside the query tuple: `all` or `{<<"a">>, <<"z">>}`.

## SegmentFilter

datatype: all or segment tuple

### Description

Segment restriction: `all` or `{segments, [0,1], small}`. The tree size must match the segment numbering.

## ModifiedRange

datatype: all or date tuple

### Description

Modification-time filter: `all`, or `{date, Start, End}` with inclusive lower and upper bounds. Each bound can be Unix seconds, or both can be Erlang calendar datetime tuples.

The unambiguous datetime **2026-12-24 23:59:59 UTC** is `{{2026,12,24},{23,59,59}}` (Unix seconds `1798156799`). For that UTC day:

```erlang
{date, {{2026,12,24},{0,0,0}}, {{2026,12,24},{23,59,59}}}
```

Use UTC: calendar tuples carry no timezone, and the conversion does not apply a local timezone offset. The Erlang AAE API does not parse date strings directly. To use an RFC3339 string, convert it first with `calendar:rfc3339_to_system_time("2026-12-24T23:59:59Z")`. The shell `riak admin tictacaae fold` command performs that RFC3339 conversion itself. Mixed integer/calendar bounds are not converted as a pair. Start must not be later than End.

## ChangeMethod

datatype: change method

### Valid values

- count
- local
- {job, JobId}

### Description

`count` reports matching keys without changing data. `local` submits the changes to the node-local workers. `{job, JobId}` uses a dedicated job, where JobId is a positive integer, for example `{job, 42}`. The reported match count is not a completion barrier: poll the resulting data before assuming every change has finished.

## NVal

datatype: positive integer

### Description

Replication factor of the tree being queried, for example `3`.

# Examples

## erlang-riak-client-aae-fold:calendar-dates

### Description

Use a calendar-date range to select objects by modification time. All five objects in this example were modified at 2026-12-24 23:59:59 UTC; a range ending at that time includes them, demonstrating the inclusive upper bound.

## erlang-riak-client-aae-fold:seed-five-objects

title: Create five objects

# Reviewed against

3.4.0: 46935506fe17be122d84fae0998679e483083c6c3ff46e99c3952c8d1a49fce2
3.4.1: 46935506fe17be122d84fae0998679e483083c6c3ff46e99c3952c8d1a49fce2

# Tags

feature: tictac-aae
repository: riak_kv
module: riak_client
concept: replica-repair
