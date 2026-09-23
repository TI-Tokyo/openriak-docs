# Metadata

command: shell:riak admin repair-2i
versions: 3.4.0, 3.4.1

# Summary

Repair secondary-index entries for selected partitions.

# Description

Repair legacy LevelDB secondary indexes using built legacy AAE trees. This requires legacy AAE to be active; it is not a Leveled/TicTac repair operation. Read status before starting or cancelling work.

# Arguments

## Idx

datatype: partition index
required: false
repeatable: true

### Description

Optional full partition indexes, separated by spaces. For example, `0` selects the zero index. Omit the indexes to repair every local partition.

# Options

## --speed

datatype: integer from 1 to 100
required: false
repeatable: false

### Description

Percentage speed limit for a repair, from 1 to 100. This controls a repair start rather than status inspection.

# Results

## reference-result-1

### Description

The start command launches maintenance work; status reports its progress and kill requests cancellation.

# Examples

## shell-riak-admin-repair-2i:show-repair-usage

### Description

Repair legacy LevelDB secondary-index entries, then check the index results. This example starts repair for all eight partitions and still returns all five indexed keys afterward.

# Reviewed against

3.4.0: f016463d7c5d39a6ee34a27f8a2aacdcc6c010875dd3b59e9f3dacc0ff37f1f2
3.4.1: f016463d7c5d39a6ee34a27f8a2aacdcc6c010875dd3b59e9f3dacc0ff37f1f2

# Tags

feature: read-repair
repository: riak_kv
module: riak_kv_console
concept: replica-repair
