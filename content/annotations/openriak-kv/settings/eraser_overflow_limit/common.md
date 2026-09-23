# Description

Maximum eraser overflow-queue size. New additions beyond the limit are discarded, so monitor bulk-delete progress when the queue is full. After changing this at runtime, `riak_kv_eraser:clear_queue()` starts a queue with the new limit and clears queued work.

# Tags

feature: deletion
repository: riak_kv
module: riak_kv_eraser
concept: queueing, tombstones

# Reviewed against

3.4.0: 1154f68b2bc982d061de508461bea8cff51b3f8b1bf91fa110c7123f652f4016
3.4.1: 128536917a4529a996937d8322c4eb463913bde66bd70be4b05f95094dc28941
