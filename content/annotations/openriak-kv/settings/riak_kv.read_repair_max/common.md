# Description

Active-GET count at or above which ordinary GET read repair is skipped. When unset, this load-based suppression is disabled; the soft threshold controls probabilistic suppression below the hard limit.

# Datatype

Integer or atom

# Units

- active GETs

# Constraints

- Non-negative integer active-GET hard limit, or `undefined` to disable limiting.

# Inferred default

Unset (`undefined`); the read-repair load cap is disabled.

# Tags

feature: read-repair
repository: riak_kv
module: riak_kv_get_fsm
concept: overload-protection, replica-repair

# Notes

This is the Erlang application environment key `read_repair_max` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_get_fsm.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_get_fsm.erl#L665)

# Reviewed against

3.4.0: 3c75c694b3553e90ebe83deb14ba2cb6b1f54852d9769a1e9ae1d2d7977b50b6
3.4.1: 3f0b4fa718149cb285bbc5c8eed83d980da2fe0843ebee786174b9619ec6397d
