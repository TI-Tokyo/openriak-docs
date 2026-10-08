# Metadata

command: shell:riak repl del-listener
versions: 3.4.0, 3.4.1

# Summary

Remove a legacy replication listener.

# Deprecation

This operation belongs to the legacy replication protocol. There is no direct replacement within that protocol. Migrate to named-cluster replication using [`riak repl connect`](../connect/) and review [`riak repl fullsync start`](../fullsync/start/) and [`riak repl fullsync stop`](../fullsync/stop/) for full-sync control.

# Description

This belongs to the deprecated replication protocol. It is documented here for historical reference; migrate existing deployments to named-cluster replication.

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

3.4.0: 8a8408d94dd3c8bb501d10445a81a6cf3ce50d35560dd18518a607beeb60e69e
3.4.1: 8a8408d94dd3c8bb501d10445a81a6cf3ce50d35560dd18518a607beeb60e69e

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_console
concept: cross-cluster-replication
