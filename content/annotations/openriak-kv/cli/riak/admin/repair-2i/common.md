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

3.4.0: 865a63fa9722bc889944db8337a13857f2cc5a222b09f42005237af3301aad5a
3.4.1: 865a63fa9722bc889944db8337a13857f2cc5a222b09f42005237af3301aad5a

# Tags

feature: read-repair
repository: riak_kv
module: riak_kv_console
concept: replica-repair
