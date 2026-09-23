# Description

Recompute partition placement when a node leaves instead of preserving as much existing placement as possible. This can avoid uneven intermediate ownership in small or location-aware clusters, but can require more transfers; inspect the cluster plan before committing.

# Tags

feature: cluster-management
repository: riak_core
module: riak_core_console, riak_core_membership_leave
concept: partition-placement

# Reviewed against

3.4.0: b84423f4cb32754ded927612acc47d213a75857f6b6e952238160eede4fbd857
3.4.1: 79604b0cb912c6f006a2d54ff1c020f2f2a184e9d945173c151586b0e77c9498
