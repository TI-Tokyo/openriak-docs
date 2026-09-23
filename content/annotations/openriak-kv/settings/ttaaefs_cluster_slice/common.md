# Description

Scheduling slice used to offset Tictac full-sync activity between clusters. Values 1–4 let connected clusters stagger checks, for example by using slices 1 and 3 for opposite directions.

# Tags

feature: full-sync
repository: riak_kv
module: riak_kv_ttaaefs_manager
concept: replica-repair

# Reviewed against

3.4.0: 6adf1962ec6dcaa76a3f609c1020a8532126c51126602f3785c47cecf3960b5c
3.4.1: 0d6a3c9fa235aa60752a35461067ccb028201f74e068375e37f6c971051541f3
