# Description

Number of legacy AAE tree builds permitted during `anti_entropy.tree.build_limit.per_timespan`. Each build scans a partition, so this rate limit controls background disk work as well as repair readiness.

# Tags

feature: legacy-aae
repository: riak_kv
module: riak_kv_entropy_manager
concept: replica-repair

# Reviewed against

3.4.0: 017051acbeb402725bf87a74f4b5d40831e6feed4d69600f96803654c7d0647e
3.4.1: 881f9e23471921b5d52be618dac43134428343fa08f55554f4dacffc217c6f8d
