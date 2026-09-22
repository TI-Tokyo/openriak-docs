# Metadata

command: shell:riak repl connect
versions: 3.4.0, 3.4.1

# Summary

Register a replication control connection.

# Description

Name the local cluster before connecting. A successful request changes connection management; use connections to check whether a remote handshake succeeds.

# Arguments

## destination

datatype: host:port
required: true
repeatable: false

### Description

Use `host:port`, for example `node2.test:9080`. Disconnect also accepts a known symbolic cluster name. Connect requires the cluster-manager endpoint, not the HTTP or Protocol Buffers port.

# Examples

## shell-riak-repl-connect:a-control-endpoint

### Description

Submit the connection-management request. If no remote cluster is listening at that endpoint, the request cannot establish a replication connection.

# Reviewed against

3.4.0: b184c4bee315072be42d09bc619a95c021d1ceac965148b7fbb2af8cf1ac6762
3.4.1: b184c4bee315072be42d09bc619a95c021d1ceac965148b7fbb2af8cf1ac6762
