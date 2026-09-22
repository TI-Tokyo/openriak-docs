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

3.4.0: 6c835990f29395f83eddf9d48cc87be18e41c44c54c3e14ac0300a061e32cad6
3.4.1: 6c835990f29395f83eddf9d48cc87be18e41c44c54c3e14ac0300a061e32cad6
