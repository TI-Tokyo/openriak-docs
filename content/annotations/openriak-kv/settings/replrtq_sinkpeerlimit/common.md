# Description

Maximum sink workers assigned to any one replication peer. This keeps a single source from consuming all workers; when unset, the effective limit follows the sink-worker count.

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_replrtq_snk
concept: cross-cluster-replication

# Reviewed against

3.4.0: d06d221b46886b9ac8a3bd273914af9f28386dd89f1a131aa4d75169669a68d0
3.4.1: e85dc0acbd1514e5cae4c7531db4b0a6692855d5c0c773229c4f9694a948f8a2
