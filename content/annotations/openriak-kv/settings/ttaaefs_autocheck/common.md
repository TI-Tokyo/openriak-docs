# Description

Number of adaptive Tictac full-sync checks per day. Each selects a range check when a useful range is known, a no-check when repair would not help, or an all/day check according to the full-check window and previous outcome.

# Tags

feature: full-sync
repository: riak_kv
module: riak_kv_ttaaefs_manager
concept: replica-repair

# Reviewed against

3.4.0: 8fb982af061ef4637899274e368419f7abc6e4fb33d60cd3fcf38c15f7b4bb5d
3.4.1: a9f0d7c3712bad1bd5ae4a6b7015fb8fb64fef7f84aa77c7553e399fd2dc7c3f
