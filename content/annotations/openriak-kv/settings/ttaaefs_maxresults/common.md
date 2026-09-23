# Description

Maximum differing AAE segments processed per Tictac full-sync exchange. Smaller values reduce individual clock-query cost but require more exchanges; range checks multiply this limit by `ttaaefs_rangeboost`.

# Tags

feature: full-sync
repository: riak_kv
module: riak_kv_ttaaefs_manager
concept: replica-repair

# Reviewed against

3.4.0: a6b1417878b5df01f6325ef4c29e585f5aba692efd23167251077394dc649eed
3.4.1: 838d1da294046a64ecf2de24e794cacc195ab65e98633ea3fefb9af244c73f52
