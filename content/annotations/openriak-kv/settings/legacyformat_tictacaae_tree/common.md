# Description

Use the older Tictac tree representation for compatibility during rolling upgrades involving per-bucket full-sync. Keep this tied to an actual mixed-version upgrade requirement rather than treating it as a performance switch.

# Tags

feature: tictac-aae
repository: riak_kv
module: riak_kv_clusteraae_fsm
concept: replica-repair

# Reviewed against

3.4.0: 7e9be6258beed52d31f10497548d178d149c6919b0424d6198272b9dc1cf2c6e
3.4.1: 9d9fc2aad9c95dad6d524f348a080d4f078be97451ebf8ae923440672cab6a43
