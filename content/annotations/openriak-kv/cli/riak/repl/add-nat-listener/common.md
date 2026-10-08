# Metadata

command: shell:riak repl add-nat-listener
versions: 3.4.0, 3.4.1

# Summary

Add a legacy replication listener behind NAT.

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

## public_ip

datatype: IP address
required: true
repeatable: false

### Description

Public address advertised to remote peers.

## public_port

datatype: integer from 1 to 65535
required: true
repeatable: false

### Description

Externally reachable listener port.

# Results

## outcome

### Description

A successful call registers a legacy listener with its advertised external address. The example uses the bundled release launcher to preserve the address and port.

# Examples

## shell-riak-repl-add-nat-listener:a-loopback-test-listener

title: A loopback listener

# Reviewed against

3.4.0: 8e4c05d648d33605710f7550de35bc650a51137633b3edf17bcf3e313c981a02
3.4.1: 8e4c05d648d33605710f7550de35bc650a51137633b3edf17bcf3e313c981a02

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_console
concept: cross-cluster-replication
