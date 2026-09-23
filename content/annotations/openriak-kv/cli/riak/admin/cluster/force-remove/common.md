# Metadata

command: shell:riak admin cluster force-remove
versions: 3.4.0, 3.4.1

# Summary

Stage removal of an unavailable cluster member.

# Description

This stages a topology change. Review `riak admin cluster plan`, then run `riak admin cluster commit` to apply the reviewed plan. Use member-status and transfers to monitor convergence. Forced changes cannot hand off data from the unavailable node; remaining replicas must provide the data.

# Arguments

## node

datatype: Erlang node name
required: true
repeatable: false

### Description

Full Erlang node name, for example `openriak-kv@node2.test`.

# Results

## reference-result-1

### Description

On success, prints a staged-change confirmation. The membership change takes effect only after planning and committing it.

# Reviewed against

3.4.0: 06a6f0aca6d67ce87f974d7931b12563850f30cae8817a9d21010d10ec328855
3.4.1: 06a6f0aca6d67ce87f974d7931b12563850f30cae8817a9d21010d10ec328855

# Tags

feature: cluster-management
repository: riak_core
module: riak_core_console
concept: partition-placement
