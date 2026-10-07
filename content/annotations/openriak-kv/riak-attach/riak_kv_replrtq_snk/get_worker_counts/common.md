# Metadata

command: erlang:riak_kv_replrtq_snk:get_worker_counts/0
versions: 3.4.0, 3.4.1

# Summary

Read default sink worker and per-peer limits.

# Description

Returns `{WorkerCount, PerPeerLimit}` from the current application environment.

# Arguments

# Reviewed against

3.4.0: eed39d24e345436622a400a5d99519f40d6873a270d906f17db3ab81e6465104
3.4.1: b9d505d4b6537630339367f011b22355917298eb2768990ddc275e016951f43d

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_replrtq_snk
concept: concurrency, cross-cluster-replication
