# Metadata

command: shell:riak repl add-listener
versions: 3.4.0, 3.4.1

# Summary

Add a legacy replication listener.

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

## shell-riak-repl-add-listener:a-loopback-test-listener

title: A loopback listener

### Description

Update the legacy listener configuration inside the node.

# Reviewed against

3.4.0: e6888c2f01078db72feb6e46c50129aeed6c14be9d7a1cee95334b45cc21411c
3.4.1: e6888c2f01078db72feb6e46c50129aeed6c14be9d7a1cee95334b45cc21411c
