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

3.4.0: c67bf982983c2950584f468b7d1cc6c17e0eeed15512fa759092514118532cb1
3.4.1: c67bf982983c2950584f468b7d1cc6c17e0eeed15512fa759092514118532cb1
