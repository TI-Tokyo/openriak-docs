# Description

Queue definitions separated by `|`, each in `name:filter` form. Filters include `any`, `block_rtq`, `bucketname.NAME`, `bucketprefix.PREFIX` and `buckettype.TYPE`. For example, `cluster_a:any|cluster_b:bucketprefix.user` selects all changes for one queue and a bucket subset for another.

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_replrtq_src
concept: cross-cluster-replication, queueing

# Reviewed against

3.4.0: c6206eaeb2910c1d89e1105fcb9617f917a0a876445cac017d41f41689cce7c9
3.4.1: 188913ae420fb89ba993cb65346c75c3164dab6e88bb98251ea8c46a3c7b34bd
