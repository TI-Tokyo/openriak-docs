# Metadata

command: shell:riak repl del-listener
versions: 3.4.0, 3.4.1

# Summary

Remove a legacy replication listener.

# Description

This belongs to the deprecated replication protocol. Use it only for an existing deployment that still requires that protocol.

# Arguments

## nodename

datatype: Erlang node name
required: true
repeatable: false

### Description

Cluster member on which the listener runs.

## listen_ip

datatype: IP address
required: true
repeatable: false

### Description

Address assigned to that node, for example `127.0.0.1`.

## port

datatype: integer from 1 to 65535
required: true
repeatable: false

### Description

Local listening port, for example `9010`.

# Examples

## shell-riak-repl-del-listener:a-loopback-test-listener

title: A loopback listener

### Description

Update the legacy listener configuration inside the node.

# Reviewed against

3.4.0: 8cf5a303c06d665a0c823a035143c53d45630aa1f41ec49252acff5b84a67db0
3.4.1: 8cf5a303c06d665a0c823a035143c53d45630aa1f41ec49252acff5b84a67db0

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_console
concept: cross-cluster-replication
