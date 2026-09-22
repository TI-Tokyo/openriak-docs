# Metadata

command: shell:riak repl nat-map del
versions: 3.4.0, 3.4.1

# Summary

Remove a replication address translation.

# Description

Maps an advertised external address to the address reachable internally. Keep port-specific mappings consistent with the destination listener.

# Arguments

## externalip

datatype: IP address or IP:port
required: true
repeatable: false

### Description

External address with an optional port, for example `203.0.113.10:9080`.

## internalip

datatype: IP address
required: true
repeatable: false

### Description

Internal address to use instead, for example `127.0.0.1`.

# Results

## outcome

### Description

A successful call removes the matching mapping from `nat-map show`. The fixture creates the mapping before removing it.

# Reviewed against

3.4.0: 1c0e499903b3aabc1eb7e8196aa41696ac67e7c6430875321691323b43d5d18b
3.4.1: 1c0e499903b3aabc1eb7e8196aa41696ac67e7c6430875321691323b43d5d18b
