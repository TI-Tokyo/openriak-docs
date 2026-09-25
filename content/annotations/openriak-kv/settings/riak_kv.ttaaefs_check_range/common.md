# Description

Current range filter for a Tictac full-sync range check. It can restrict the bucket, key range, modification-time range and tree segments; `none` means no saved range. Range-management operations update this value.

# Datatype

Atom or tuple

# Constraints

- `none` or `{Bucket, KeyRange, DateRange, SegmentFilter}`. Bucket is a binary or `{TypeBinary, BucketBinary}`, or `all`; KeyRange is `{StartKey, EndKey}` or `all`; DateRange is `{LowEpochSeconds, HighEpochSeconds}` or `all`; SegmentFilter is `{segments, SegmentIds, TreeSize}` or `all`. Managed by the range API.

# Inferred default

`none`.

# Tags

feature: full-sync
repository: riak_kv
module: riak_kv_ttaaefs_manager
concept: querying, cross-cluster-replication

# Notes

This is the Erlang application environment key `ttaaefs_check_range` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_ttaaefs_manager.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_ttaaefs_manager.erl#L956)

# Reviewed against

3.4.0: f47845ceb82f2484345f56be0feaf7b763cb149fe1479d75350a665939e819a1
3.4.1: 0f6dc66f4403399b0ace176a8fb7bd38e6deb7fb542b64f6531c16664a8bdd54
