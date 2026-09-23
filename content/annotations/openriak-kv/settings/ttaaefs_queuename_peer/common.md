# Description

Remote replication queue this cluster consumes for bidirectional full-sync repair. Providing the peer queue lets discovered differences prompt repairs in both directions; `disabled` keeps repair unidirectional.

# Tags

feature: full-sync
repository: riak_kv
module: riak_kv_ttaaefs_manager
concept: queueing, replica-repair

# Reviewed against

3.4.0: 06f97de371a0a2c23fafbb90a75d45a53bcc5a88a7f5b721947e8b512d6c8f8d
3.4.1: d8beefc72bf2771f23e697bd44da840db93ac2d9fda881973e0724889a7cf38a
