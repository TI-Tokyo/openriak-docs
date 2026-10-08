# Metadata

command: shell:riak repl disconnect
versions: 3.4.0, 3.4.1

# Summary

Remove a replication control connection.

# Description

Name the local cluster before connecting. A successful request changes connection management; use connections to check whether a remote handshake succeeds.

# Arguments

## destination

datatype: host:port or cluster name
required: true
repeatable: false

### Description

Use `host:port`, for example `node2.test:9080`. Disconnect also accepts a known symbolic cluster name. Connect requires the cluster-manager endpoint, not the HTTP or Protocol Buffers port.

# Examples

## shell-riak-repl-disconnect:a-control-endpoint

### Description

Submit the connection-management request. If no remote cluster is listening at that endpoint, the request cannot establish a replication connection.

# Reviewed against

3.4.0: 5cf35f0d54d31baec22ece29368520961eca5d2e9da1602e021f266dea999c54
3.4.1: 5cf35f0d54d31baec22ece29368520961eca5d2e9da1602e021f266dea999c54

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_console
concept: cross-cluster-replication
