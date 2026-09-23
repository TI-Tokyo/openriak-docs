# Description

Client certificate presented by this node to an authenticated replication peer. The remote cluster must trust it; the matching private key is configured through `repl_key_filename`.

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_replrtq_snk, riak_kv_ttaaefs_manager
concept: cross-cluster-replication, tls

# Reviewed against

3.4.0: 490e973f04c10002c9c70ff6ff83ed84491963f564c09a256bdd37411ab1031c
3.4.1: 721d94f27f2956c1f583a8ab053869e548dd1a7e4dba0fde829c5d09ed538053
