# Description

Action timeout, in milliseconds, used by legacy anti-entropy exchange state machines. Legacy replication's AAE full-sync source also reads this value when coordinating a tree exchange.

# Datatype

Timeout

# Units

- milliseconds

# Constraints

- Non-negative integer state-machine timeout, or `infinity`.

# Inferred default

Consumer-dependent: `60000` for local KV AAE exchanges and `300000` for replication AAE source exchanges. Setting the key overrides both fallbacks.

# Tags

feature: legacy-aae, full-sync
repository: riak_kv, riak_repl
module: riak_kv_exchange_fsm, riak_repl_aae_source
concept: replica-repair

# Notes

This is the Erlang application environment key `anti_entropy_timeout` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_exchange_fsm.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_exchange_fsm.erl#L77)
- [riak_repl/src/riak_repl_aae_source.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_aae_source.erl#L197)

# Reviewed against

3.4.0: 9d9d6bcd9463d8d1c893e213aef875a0a9218b3f15da5b8965d3349d51f1c650
3.4.1: a5efd2bb8ad5fe8e0fc169a22af89e82d640704e97e3cad69bc500ec8b1e69aa
