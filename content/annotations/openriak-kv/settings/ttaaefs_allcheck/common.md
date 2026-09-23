# Description

Number of full-data Tictac full-sync checks scheduled per day. An n_val check compares the corresponding replica set across clusters; a bucket-scoped check scans that bucket. Large checks can consume substantial query capacity and delay other checks.

# Tags

feature: full-sync
repository: riak_kv
module: riak_kv_ttaaefs_manager
concept: replica-repair

# Reviewed against

3.4.0: 4168f84c0082735380dc4e6ac5886787cab07e43811196d8656a7c665101631a
3.4.1: bd8d2bab0dd1c7c941a2c53dc94f5c392baab8b9a934c8b4c364f87ffd21192e
