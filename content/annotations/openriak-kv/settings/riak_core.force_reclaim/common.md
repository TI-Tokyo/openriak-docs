# Description

One-shot request to rerun the version 3 partition-claim algorithm even when the existing ownership might otherwise be accepted. The claim code unsets the flag after consuming it.

# Datatype

Boolean

# Allowed values

- `true`
- `false`

# Constraints

- Use the Erlang atoms `true` or `false`.

# Inferred default

`false`.

# Tags

feature: cluster-management
repository: riak_core
module: riak_core_membership_claim
concept: partition-placement

# Notes

This is the Erlang application environment key `force_reclaim` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_membership_claim.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_membership_claim.erl#L302)

# Reviewed against

3.4.0: cfbc0ac99853985872c560ea7c0753e12f6371f036be882090d05b29b3feb52a
3.4.1: cfbc0ac99853985872c560ea7c0753e12f6371f036be882090d05b29b3feb52a
