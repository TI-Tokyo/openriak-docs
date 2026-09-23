# Description

Maximum object count cached in a replication priority queue. Beyond it, entries retain clocks and the object is fetched again when replicated; this controls memory use without excluding those objects from replication.

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_replrtq_src
concept: cross-cluster-replication

# Reviewed against

3.4.0: fb17bdd336439c3060713ad9e9ed1821a51377e11ff14644eafbf43da849723f
3.4.1: d81d9acf1e0e5d41ce9d0cfa7a2a4b647f0e0449b52d08c79daf4b036f83e324
