# Description

Choose the partition-claim algorithm used for cluster membership changes. `choose_claim_v2` targets ordinary placement; `choose_claim_v3` is deprecated; `choose_claim_v4` supports location-aware planning. Review the resulting cluster plan before committing it.

# Tags

feature: cluster-management
repository: riak_core
module: riak_core_claim_sim, riak_core_membership_claim, riak_core_membership_leave
concept: partition-placement

# Reviewed against

3.4.0: f69ce62e10f83beda23cf907957b7de07fe53526339e5e096da248cb818f0807
3.4.1: 22d7c2c73834acdbbb82512a96d61209c2e222bc9c3445619180e68e2641b76f
