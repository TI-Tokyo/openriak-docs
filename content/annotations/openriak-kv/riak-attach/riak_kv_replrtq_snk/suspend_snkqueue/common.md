# Metadata

command: erlang:riak_kv_replrtq_snk:suspend_snkqueue/1
versions: 3.4.0, 3.4.1

# Summary

Suspend workers for a sink queue.

# Description

Pause fetching for this queue across its configured peers. Resume when maintenance is complete.

# Arguments

## QueueName

datatype: Erlang atom
required: true
repeatable: false

### Description

See the shared `QueueName` argument on the parent module page.

# Reviewed against

3.4.0: 5ceaf4968dff70a0545f63f61e01a4d3ea13636ebd59ec2f7fc6375327b81314
3.4.1: 5ceaf4968dff70a0545f63f61e01a4d3ea13636ebd59ec2f7fc6375327b81314
