# Description

Restrict read repair to primary vnodes. This avoids copying historical data onto short-lived fallbacks and reduces recovery handoff work, but leaves fallbacks without the extra resilience and repeated-read benefit of repaired data.

# Tags

feature: read-repair
repository: riak_kv
module: riak_kv_get_fsm
concept: replica-repair

# Reviewed against

3.4.0: d5e53107a0658e637333fb32acd1d34bbe459be9e036e1ef8346ca0c7a1bcfe3
3.4.1: 55e01d981538d8065f6fb5853d65d21646c9bbf5100d4633aed9710d68bfb473
