# Metadata

command: erlang:riak_kv_ttaaefs_manager:set_range/4
versions: 3.4.0, 3.4.1

# Summary

Set a bucket, key and modification-time range for full-sync.

# Description

This legacy entry point converts calendar datetimes into the current range representation. It does not start a sync by itself.

# Notes

These settings affect the current node. Runtime environment changes are not a replacement for persistent configuration.

# Arguments

## Bucket

datatype: bucket or all
required: true
repeatable: false

### Description

Bucket binary, a typed-bucket pair, or `all` for all buckets.

## KeyRange

datatype: pair of binaries or all
required: true
repeatable: false

### Description

Inclusive key bounds as `{<<"a">>, <<"z">>}`, or `all`.

## LowDateTime

datatype: calendar datetime
required: true
repeatable: false

### Description

Beginning of the UTC modification interval, for example `{{2026,12,24},{0,0,0}}`.

## HighDateTime

datatype: calendar datetime
required: true
repeatable: false

### Description

End of the UTC modification interval, for example `{{2026,12,24},{23,59,59}}` for 2026-12-24 23:59:59 UTC. Calendar tuples have no timezone field.

# Reviewed against

3.4.0: 82847b50e2e2b4a64ae2c734560e7ce9a1172dd1fb9b96425fe8bf6b8c68a263
3.4.1: 7216094212cc7333b5b4d69c54b8a48566f8b1471d0db1c384db5852084ec62c

# Tags

feature: full-sync
repository: riak_kv
module: riak_kv_ttaaefs_manager
concept: replica-repair
