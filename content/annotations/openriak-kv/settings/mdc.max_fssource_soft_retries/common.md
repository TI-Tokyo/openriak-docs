# Description

Number of soft failures the full-sync coordinator tolerates before failing work. The budget is per full-sync, not a separate allowance per partition; combine it with `mdc.fssource_retry_wait` to avoid rapid retry exhaustion.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl2_fscoordinator
concept: cross-cluster-replication

# Reviewed against

3.4.0: e82055de219b832bb1b30bc15c8cac5fd8cdda7a1eb7fbf8ff45122a879f52ef
3.4.1: e82055de219b832bb1b30bc15c8cac5fd8cdda7a1eb7fbf8ff45122a879f52ef
