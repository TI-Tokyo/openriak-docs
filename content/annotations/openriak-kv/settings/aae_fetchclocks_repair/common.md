# Description

Repair inconsistent Tictac AAE tree segments while fetching clocks during an n_val exchange, as well as repairing object differences. Enabling this changes fetch-clock concurrency; use it when tree differences persist after object repair.

# Tags

feature: tictac-aae
repository: riak_kv
module: riak_kv_ttaaefs_manager
concept: replica-repair

# Reviewed against

3.4.0: 1f3456db96b32007d1f355f5a26c57428e4396674b570f2fca85267f33853894
3.4.1: 9be6a153a1067952f522bf64b5bb9bbcea57af4bc9fe8da61435b5b4390ff43f
