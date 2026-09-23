# Description

Obsolete queue-size setting retained for compatibility. These releases use disk-backed overflow queues and ignore this limit; configure `replrtq_overflow_limit` instead.

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv.schema
concept: cross-cluster-replication, queueing

# Reviewed against

3.4.0: baa9d0e0c1b48fa844dff832821e0936b7f3ca4f99667dc60e1e0aa83d10b61a
3.4.1: 299c1a75dd0df209471d562639ee72ef5f074c8fae58ed24b3ff537751351c50
