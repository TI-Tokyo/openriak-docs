# Metadata

command: erlang:riak_kv_replrtq_snk:get_worker_counts/0
versions: 3.4.0, 3.4.1

# Summary

Read default sink worker and per-peer limits.

# Description

Returns `{WorkerCount, PerPeerLimit}` from the current application environment.

# Arguments

# Reviewed against

3.4.0: b9d505d4b6537630339367f011b22355917298eb2768990ddc275e016951f43d
3.4.1: b9d505d4b6537630339367f011b22355917298eb2768990ddc275e016951f43d

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_replrtq_snk
concept: concurrency, cross-cluster-replication
