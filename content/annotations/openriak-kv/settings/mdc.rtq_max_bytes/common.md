# Description

Maximum byte size of the legacy real-time replication queue. New objects are dropped once it fills; a later full-sync is needed to reconcile changes missed by real-time delivery.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl2_rtq
concept: cross-cluster-replication

# Reviewed against

3.4.0: 25b08bb69594675884a6530f64f816448605b6cc756d8454027f2e0e9a113c88
3.4.1: 25b08bb69594675884a6530f64f816448605b6cc756d8454027f2e0e9a113c88
