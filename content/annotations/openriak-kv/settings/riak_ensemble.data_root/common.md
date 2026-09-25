# Description

Root directory for persisted ensemble state, including ensemble facts, peer hash trees and the basic backend's data files. These files are stored beneath its `ensembles` subdirectory.

# Datatype

Directory path

# Constraints

- Writable directory path for ensemble state.

# Inferred default

Set by `riak_ensemble_sup:start_link/1`; Riak Core supplies `riak_core.platform_data_dir`. The consumers have no independent fallback.

# Tags

feature: strong-consistency
repository: riak_ensemble
module: riak_ensemble_basic_backend, riak_ensemble_peer, riak_ensemble_storage
concept: filesystem-layout, consensus

# Notes

This is the Erlang application environment key `data_root` in `riak_ensemble`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_ensemble/src/riak_ensemble_basic_backend.erl](https://github.com/OpenRiak/riak_ensemble/blob/ed6d4cfcf107385d3e0b6f7517a9a46c7104abbe/src/riak_ensemble_basic_backend.erl#L66)
- [riak_ensemble/src/riak_ensemble_peer.erl](https://github.com/OpenRiak/riak_ensemble/blob/ed6d4cfcf107385d3e0b6f7517a9a46c7104abbe/src/riak_ensemble_peer.erl#L2180)
- [riak_ensemble/src/riak_ensemble_storage.erl](https://github.com/OpenRiak/riak_ensemble/blob/ed6d4cfcf107385d3e0b6f7517a9a46c7104abbe/src/riak_ensemble_storage.erl#L111)

Additional type/default evidence:

- [riak_core/src/riak_core_sup.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_sup.erl)
- [riak_ensemble/src/riak_ensemble_sup.erl](https://github.com/OpenRiak/riak_ensemble/blob/ed6d4cfcf107385d3e0b6f7517a9a46c7104abbe/src/riak_ensemble_sup.erl)

# Reviewed against

3.4.0: 805d910134b57d60b366ce4cadd799f9f85d8a378596b5386f3db5fe1f45bc41
3.4.1: 805d910134b57d60b366ce4cadd799f9f85d8a378596b5386f3db5fe1f45bc41
