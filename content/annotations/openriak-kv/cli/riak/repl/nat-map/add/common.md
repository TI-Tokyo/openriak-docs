# Metadata

command: shell:riak repl nat-map add
versions: 3.4.0, 3.4.1

# Summary

Add a replication address translation.

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

A successful call records an internal/external address mapping visible with `nat-map show`. The example uses the bundled release launcher to preserve the numeric address.

# Reviewed against

3.4.0: 783265ca68496033a566c04c777391d77b48be374cea260aa629185bf6d786f2
3.4.1: 783265ca68496033a566c04c777391d77b48be374cea260aa629185bf6d786f2

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_console
concept: cross-cluster-replication
