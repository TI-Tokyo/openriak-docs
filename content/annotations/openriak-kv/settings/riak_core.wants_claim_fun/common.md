# Description

`{Module, Function}` callback used by the partition-claim algorithm to decide whether a node needs more partitions. It works with the configured claim-selection function to balance ownership.

# Datatype

Tuple

# Constraints

- `{Module, Function}` atom pair for the partition-claim decision callback.

# Inferred default

`{riak_core_membership_claim, default_wants_claim}` from `riak_core.app.src`.

# Tags

feature: cluster-management
repository: riak_core
module: riak_core_claim_sim, riak_core_membership_claim
concept: partition-placement

# Notes

This is the Erlang application environment key `wants_claim_fun` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_claim_sim.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_claim_sim.erl#L108)
- [riak_core/src/riak_core_membership_claim.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_membership_claim.erl#L104)

Additional type/default evidence:

- [riak_core/src/riak_core.app.src](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core.app.src)

# Reviewed against

3.4.0: 7b068f489b75dde400c718862de5f6c12350c29ecba1df627c42fe876a535de9
3.4.1: 7b068f489b75dde400c718862de5f6c12350c29ecba1df627c42fe876a535de9
