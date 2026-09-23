# Description

Allow this node to answer coverage queries, including secondary-index queries. Disable temporarily when its data is incomplete during repair or replacement, then restore participation after recovery.

# Tags

feature: secondary-indexes
repository: riak_kv
module: riak_client, riak_core, riak_core_ring_manager
concept: querying

# Reviewed against

3.4.0: b10199321cfc5a57c42ee551e376f173851a84ce6d6b22de80624814e9367555
3.4.1: 4516f028f94d320b78e91896c8fae70faa41d9eeb17fbea7ed17b8a1c44ebcc3
