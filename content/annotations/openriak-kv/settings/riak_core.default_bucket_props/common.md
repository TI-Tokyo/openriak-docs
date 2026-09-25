# Description

Application-level list of default bucket properties, including replication and quorum values. Untyped bucket operations use these as fallbacks, and ring placement checks use the default `n_val`; typed buckets use their resolved type properties instead.

# Datatype

List

# Constraints

- Property list of `{PropertyAtom, Value}` pairs. Values must satisfy the relevant bucket-property validator; for example, `n_val` is a positive replica count.

# Inferred default

Assembled by bucket-property initialization and registered applications; no single fixed list. Append operations start from `[]`, while normal object operations expect initialization to have populated the key.

# Tags

feature: bucket-properties
repository: riak_core, riak_kv, riak_repl
module: riak_core_bucket_props, riak_core_location, riak_core_ring_manager, riak_core_ring_util, riak_kv_get_fsm, riak_kv_put_fsm, riak_repl2_fscoordinator, riak_repl_rtenqueue
concept: data-policy, quorums

# Notes

This is the Erlang application environment key `default_bucket_props` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_bucket_props.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_bucket_props.erl#L110)
- [riak_core/src/riak_core_location.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_location.erl#L83)
- [riak_core/src/riak_core_ring_manager.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_ring_manager.erl#L605)
- [riak_core/src/riak_core_ring_util.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_ring_util.erl#L56)
- [riak_kv/src/riak_kv_get_fsm.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_get_fsm.erl#L260)
- [riak_kv/src/riak_kv_put_fsm.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_put_fsm.erl#L1020)
- [riak_repl/src/riak_repl2_fscoordinator.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl2_fscoordinator.erl#L903)
- [riak_repl/src/riak_repl_rtenqueue.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_rtenqueue.erl#L114)

# Reviewed against

3.4.0: 9332e1b76eee79f152d803981dce7c12140bc18a4255394d7cf9b13ab901f31b
3.4.1: 7d25315cdddffe706eef8c0cb89900f1e60e0ffd8d1a49dcbce3e547da536ecf
