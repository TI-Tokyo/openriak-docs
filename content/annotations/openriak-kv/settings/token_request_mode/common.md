# Description

Verification mode for conditional-write tokens. `head_only` trusts the current preference-list head; `basic_consensus` checks other available nodes; `primary_consensus` requires agreement from primary nodes and a sufficient placement target. None of these modes provides strict guarantees through every network-partition scenario.

# Tags

feature: conditional-writes
repository: riak_kv
module: riak_kv_token_session
concept: concurrency-control

# Reviewed against

3.4.0: df594b10bf5a3341face8819600868b019a8f78237dd8366318cf5a983dde017
3.4.1: eab9d9fcd5795b22b1b8f3b6d3a89a640dfc30f3fec7f035e93fe7a9b3fc81fc
