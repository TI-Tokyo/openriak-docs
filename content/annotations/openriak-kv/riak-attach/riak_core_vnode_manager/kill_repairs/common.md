# Metadata

command: erlang:riak_core_vnode_manager:kill_repairs/1
versions: 3.4.0, 3.4.1

# Summary

Cancel partition-repair transfers targeting this node.

# Description

Sends an asynchronous cancellation message to the vnode manager. The acknowledgment means the request was sent; it does not wait for every transfer to stop.

# Notes

This is an internal administrative API. Use the version’s node-repair CLI when it is available.

# Arguments

## Reason

datatype: Erlang term
required: true
repeatable: false

### Description

Reason recorded for the cancellation, for example `maintenance`.

# Reviewed against

3.4.0: 66ed61739e299f7d3b34f4366af5570e8bb89c950e72cb3c7c3370db26087c21
3.4.1: 66ed61739e299f7d3b34f4366af5570e8bb89c950e72cb3c7c3370db26087c21

# Tags

feature: read-repair
repository: riak_core
module: riak_core_vnode_manager
concept: replica-repair
