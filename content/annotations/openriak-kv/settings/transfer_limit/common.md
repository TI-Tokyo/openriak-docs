# Description

Node-level limit on concurrent transfers. Higher concurrency can move data faster but increases pressure; if acknowledgements time out, investigate batch size, backend pauses and handoff timeout. Scheduled transfers also obey `cluster_transfer_limit`.

# Tags

feature: handoff
repository: riak_core
module: riak_core_handoff_manager
concept: partition-transfer

# Reviewed against

3.4.0: f36cb9765726bad64136873404353235dc912673707589e8bdd754c89e174a27
3.4.1: cb47f699d86037037997287862d0511bfb35a3be29c1e1ebcce250cf1ea1b189
