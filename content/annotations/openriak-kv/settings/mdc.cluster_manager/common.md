# Description

IP address and port where the legacy multi-datacenter replication cluster manager listens. Supply an IP address rather than a hostname. Each node runs a manager, but the current cluster leader services these requests.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_core_service_mgr, riak_repl2_ip
concept: cross-cluster-replication

# Reviewed against

3.4.0: 63205c87e5db71fae1e3308f914a0d97e242783bf62e3c3ec64f5c6f9f25cccb
3.4.1: 63205c87e5db71fae1e3308f914a0d97e242783bf62e3c3ec64f5c6f9f25cccb
