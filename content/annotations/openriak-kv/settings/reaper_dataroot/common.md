# Description

Directory for the reaper's disk-backed overflow queue. It stores pending tombstone-removal work, rather than the retained tombstones in the backend.

# Tags

feature: deletion
repository: riak_kv
module: riak_kv_reaper
concept: filesystem-layout, tombstones

# Reviewed against

3.4.0: db6133305b637627377db92f400a280541ccdc0619d4c2d1541a91bc0631b737
3.4.1: b45eb5fd950e469e6f7e9e1612db6e168340b1b19e42a7333d9ddcc8e1c1e1a0
