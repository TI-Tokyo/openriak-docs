# Description

Allow reads to stop early when a majority of replicas report the key missing. This optimization is used with `notfound_ok = false`; it changes handling of missing responses rather than the stored replica count.

# Tags

feature: bucket-properties
repository: riak_kv
module: riak_kv.schema
concept: data-policy, quorums

# Reviewed against

3.4.0: 23e55956d7f9cd7c6545c3402af1c8303d2d09a942a4af7b6a1c3e9fb4d51840
3.4.1: 3bc8dbd368973d15f46b0ee86d31e8457e8d3ec9f338befa7324e91bf4aef246
