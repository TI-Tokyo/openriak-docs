# Metadata

command: erlang:riak_kv_replrtq_snk:set_worker_counts/2
versions: 3.4.0, 3.4.1

# Summary

Change the runtime defaults for sink worker counts.

# Description

Changes the default worker count and per-peer limit in the application environment. Use set_workercount to change an already configured queue.

# Arguments

## SnkWorkerCount

datatype: non-negative integer
required: true
repeatable: false

### Description

Default number of sink workers, for example `2`.

## PerPeerLimit

datatype: non-negative integer
required: true
repeatable: false

### Description

See the shared `PerPeerLimit` argument on the parent module page.

# Reviewed against

3.4.0: cf28447e60abe9f1981afc4900f06b1f4ff1d4ea0ba14ba5414bb7586b258168
3.4.1: cf28447e60abe9f1981afc4900f06b1f4ff1d4ea0ba14ba5414bb7586b258168

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_replrtq_snk
concept: concurrency, cross-cluster-replication
