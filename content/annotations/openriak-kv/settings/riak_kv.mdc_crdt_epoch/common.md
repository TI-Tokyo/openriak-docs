# Description

Setting this to integer `1` forces epoch-1 CRDT serialization for compatibility with older replication peers. Other values allow the cluster-negotiated CRDT format epoch to determine serialization.

# Datatype

Integer or atom

# Constraints

- Integer `1` forces epoch 1 encoding; any other term leaves selection to the negotiated capability.

# Inferred default

Unset (`undefined`); use the negotiated CRDT capability epoch.

# Tags

feature: data-types
repository: riak_kv
module: riak_kv_crdt
concept: compatibility, cross-cluster-replication

# Notes

This is the Erlang application environment key `mdc_crdt_epoch` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_crdt.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_crdt.erl#L535)

# Reviewed against

3.4.0: a495704f65a5e5a8bee27a8f006abaaa2d3959f7c5db1598ae732ab61926d338
3.4.1: 9feb98e0670278dbe00a52925aab6d5bf3644e960e84f59a4ef8f822b682d32c
