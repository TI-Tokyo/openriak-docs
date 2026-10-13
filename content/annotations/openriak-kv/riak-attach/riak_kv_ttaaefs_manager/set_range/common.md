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

3.4.0: a4f47d3f033f8f3a20e0ea5eebe0c29e71a5f0383308e56a1a550bcf53408933
3.4.1: 1b39f9ed8b9ff46208abfc62040612d8c7ae9bd0417e42290f7395c51232e3a4

# Tags

feature: full-sync
repository: riak_kv
module: riak_kv_ttaaefs_manager
concept: replica-repair
