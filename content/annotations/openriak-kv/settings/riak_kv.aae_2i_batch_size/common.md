# Description

Number of secondary-index entries processed per batch by the legacy 2i anti-entropy repair scan. Batching controls when the scan reports progress and applies duty-cycle pauses.

# Datatype

Integer

# Units

- objects

# Constraints

- Expected to be a positive integer scan batch size.

# Inferred default

`1000`.

# Tags

feature: secondary-indexes
repository: riak_kv
module: riak_kv_2i_aae
concept: replica-repair

# Notes

This is the Erlang application environment key `aae_2i_batch_size` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_2i_aae.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_2i_aae.erl#L324)

# Reviewed against

3.4.0: 691b7d34fdb2ec37dc363dc8852f208c1cd39086513c8348279ac7dfa93ba701
3.4.1: 158b46ee4f187fd9c0aa115f8ca517ba3271a09a110c847ad68f750704b9f56d
