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

3.4.0: 2c940c8e299894b5c64b805967050ee45bee23396990b714a3c9c564b74b2495
3.4.1: 2c940c8e299894b5c64b805967050ee45bee23396990b714a3c9c564b74b2495

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_console
concept: cross-cluster-replication
