# Description

Private key corresponding to `repl_cert_filename`. Keep it readable by the Riak service account and protected from other users; it authenticates this node's replication client.

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_replrtq_snk, riak_kv_ttaaefs_manager
concept: cross-cluster-replication

# Reviewed against

3.4.0: bb21bf641d4a21102a445b79e32dcd2ffb84f57e665fe4f0ce51bbc78153930f
3.4.1: 727808e8972f1cfe01d11793949821e9c44d63345e89515969e5e6bba5be0b2c
