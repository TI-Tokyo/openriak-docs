# Description

Multiplier applied to `tictacaae_maxresults` during range-limited repair loops after the initial exchange. Scoped queries can compare more leaves efficiently; increasing the multiplier still increases the work in each follow-up loop.

# Tags

feature: tictac-aae
repository: riak_kv
module: riak_kv_tictacaae_repairs
concept: replica-repair

# Reviewed against

3.4.0: 3d88c24753c2288606014a2deaf9b74c10f7582853f74795df620f6a3bf4af34
3.4.1: 65fd557cdc657171b5e0bf6b19244cc756047e43db15e5f757e5d7c259861667
