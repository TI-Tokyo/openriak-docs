# Description

Interval, in milliseconds, between maintenance ticks for the cluster metadata hash tree. These ticks drive its background tree maintenance.

# Datatype

Integer

# Units

- milliseconds

# Constraints

- Expected to be a non-negative integer timer delay.

# Inferred default

`10000`.

# Tags

feature: cluster-management
repository: riak_core
module: riak_core_metadata_hashtree
concept: replica-repair, scheduling

# Notes

This is the Erlang application environment key `metadata_hashtree_timer` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_metadata_hashtree.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_metadata_hashtree.erl#L368)

# Reviewed against

3.4.0: 1af7e7dd47af9e900bad523f45b9cc3070da8a87f118e72ce7e7a5bf80248494
3.4.1: 1af7e7dd47af9e900bad523f45b9cc3070da8a87f118e72ce7e7a5bf80248494
