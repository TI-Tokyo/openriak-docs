# Description

Interval, in milliseconds, between capability negotiation ticks. These ticks refresh the capabilities supported by cluster members and the negotiated feature choices.

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
module: riak_core_capability
concept: compatibility, scheduling

# Notes

This is the Erlang application environment key `capability_tick` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_capability.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_capability.erl#L262)

# Reviewed against

3.4.0: 520e923149f422d1d36c04fd6f515993853c2f3c1dcb95eb2345bd1a948d1818
3.4.1: 520e923149f422d1d36c04fd6f515993853c2f3c1dcb95eb2345bd1a948d1818
