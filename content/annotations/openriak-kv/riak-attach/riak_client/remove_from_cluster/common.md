# Metadata

command: erlang:riak_client:remove_from_cluster/2
versions: 3.4.0, 3.4.1

# Summary

Request legacy removal of a cluster member.

# Description

Invokes the legacy gossip removal path on the client’s node. Prefer staged cluster leave/force-remove commands for operational membership changes.

# Arguments

## ExitingNode

datatype: Erlang node atom
required: true
repeatable: false

### Description

Full Erlang name of the member to remove.

## Client

datatype: riak_client handle
required: true
repeatable: false

### Description

See the shared `Client` argument on the parent module page.

# Examples

## reference-example-1

title: Use staged removal

### Invocation

```erlang
riak_client:remove_from_cluster('openriak-kv@node2.test', Client).
```

### Description

Legacy API form, only for a controlled maintenance procedure. For normal operations use the corresponding staged CLI command.

### Expected output

The legacy removal RPC result; ownership recovery is asynchronous.

# Errors

## reference-error-1

### Condition

The target node is not a valid removable member or the client node cannot be reached.

### Description

The membership function returns an error or the RPC returns badrpc.

### Remedy

Check member-status and use the staged membership workflow for the intended removal.

# Results

## reference-result-1

### Description

Requests redistribution of the exiting member’s partitions. The RPC response does not establish completed recovery.

# Reviewed against

3.4.0: cebb9deca86866a858404f7de4f1f7c5c2b645dfdacb5cea987c152d2ef40e83
3.4.1: cebb9deca86866a858404f7de4f1f7c5c2b645dfdacb5cea987c152d2ef40e83
