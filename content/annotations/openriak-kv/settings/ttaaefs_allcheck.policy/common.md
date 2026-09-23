# Description

Control when an adaptive full-sync `autocheck` may escalate to an all-data check: always, never, or within the configured daily window. This does not constrain explicitly scheduled `ttaaefs_allcheck` runs.

# Tags

feature: full-sync
repository: riak_kv
module: riak_kv_ttaaefs_manager
concept: replica-repair

# Reviewed against

3.4.0: 5dd4ef16aada491f5cdfec540d2870696d9afbc684edbf5a3e307e66df16b6d5
3.4.1: 8d9315ca5726f97e2754c4462f89f02c8f2c893ddda05b92f07b368d5cba3293
