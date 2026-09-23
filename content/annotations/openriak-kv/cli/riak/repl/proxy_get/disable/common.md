# Metadata

command: shell:riak repl proxy_get disable
versions: 3.4.0, 3.4.1

# Summary

Disable proxy get for a remote cluster.

# Description

Proxy GET enables Riak CS block fetching from another cluster. It does not enable ordinary KV read forwarding.

# Arguments

## clustername

datatype: cluster name
required: true
repeatable: false

### Description

Remote symbolic cluster name, for example `cli_remote`. This is distinct from an Erlang node name or a generated cluster ID.

# Errors

## reference-error-1

### Condition

The remote cluster has no usable connection or its coordinator is unavailable.

### Description

Configuration may be accepted while no data is transferred. A failed coordinator RPC can also be printed by the launcher.

### Remedy

Inspect repl connections and repl status, confirm the remote name, and restore transport connectivity before expecting replication progress.

# Results

## outcome

### Description

The command updates the proxy-get configuration for the named destination. Check `riak repl status` for the resulting `proxy_get_enabled` list; accepting configuration does not establish a remote connection.

# Reviewed against

3.4.0: 75f91c74e86d94e2bea810833633bc363b187749768ff3c0cc6f3ab55e93f424
3.4.1: 75f91c74e86d94e2bea810833633bc363b187749768ff3c0cc6f3ab55e93f424

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_console
concept: cross-cluster-replication
