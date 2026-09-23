# Description

Maximum delay in seconds between replication peer-discovery prompts. An immediate rediscovery can be requested through `riak_client:replrtq_reset_all_peers/1`; the setting does not change replication request timeouts.

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_replrtq_peer
concept: cross-cluster-replication

# Reviewed against

3.4.0: 7d28968eaf8fe7d68676860b42087cd865bddeebd823579369ea7c4418a81014
3.4.1: 8d3e8b75f6d52d0ad05ad6b81df9ce4c1663eb1e33f1d732c6e1f0ce51c7145e
