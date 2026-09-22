# Metadata

command: shell:riak repl add-nat-listener
versions: 3.4.0, 3.4.1

# Summary

Add a legacy replication listener behind NAT.

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

3.4.0: dd5fdc8f4038cab1c49fed565ec085387de22613d6b558066c719fb5045576fd
3.4.1: dd5fdc8f4038cab1c49fed565ec085387de22613d6b558066c719fb5045576fd
