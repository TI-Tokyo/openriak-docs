# Description

Select the legacy active anti-entropy mode. `active` repairs divergent replicas in the background; `passive` leaves repair to reads; `active-debug` adds verbose diagnostic output. Tictac AAE has a separate switch, `tictacaae_active`.

# Tags

feature: legacy-aae
repository: riak_kv
module: riak_kv_entropy_manager
concept: replica-repair

# Reviewed against

3.4.0: 926d28ea8fc4bf4c0e58f30e95a5cdc575ac1e5b3d2d3ce3e64879ac3cd84f1c
3.4.1: 0ad055a4ffc97267b6c3ad2c6048502893457deec6f9efa298c21b241bc4c482
