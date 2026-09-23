# Description

Discover additional source peers from the configured replication seeds. Rediscovery is randomized between 60 seconds and `replrtq_prompt_max_seconds`; exceptional conditions fall back to configured peers.

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_replrtq_peer
concept: cross-cluster-replication

# Reviewed against

3.4.0: 339a89abd7bf35f49e23ad65e252bdeea0af7ea7790f6f6bf5522ce864a4f160
3.4.1: 3d5b04b822c72640c013a7a8ef834b9adcfab148dc857aa2edca94ec7a92c98a
