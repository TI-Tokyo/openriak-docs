# Metadata

command: shell:riak repl add-site
versions: 3.4.0, 3.4.1

# Summary

Add a legacy replication site.

# Deprecation

This operation belongs to the legacy replication protocol. There is no direct replacement within that protocol. Migrate to named-cluster replication using [`riak repl connect`](../connect/) and review [`riak repl fullsync start`](../fullsync/start/) and [`riak repl fullsync stop`](../fullsync/stop/) for full-sync control.

# Description

This configures the deprecated replication protocol. Use named-cluster connections for current replication deployments.

# Arguments

## ipaddr

datatype: IP address
required: true
repeatable: false

### Description

Remote listener address.

## portnum

datatype: integer from 1 to 65535
required: true
repeatable: false

### Description

Remote listener port.

## sitename

datatype: site name
required: true
repeatable: false

### Description

Legacy site label, for example `cli_site`.

# Reviewed against

3.4.0: 5e5c32139a4ce4b4b5c71584b11d8c09dc18ee49c839286c503fa2db7c8dd776
3.4.1: 5e5c32139a4ce4b4b5c71584b11d8c09dc18ee49c839286c503fa2db7c8dd776

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_console
concept: cross-cluster-replication
