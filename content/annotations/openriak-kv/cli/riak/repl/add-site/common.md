# Metadata

command: shell:riak repl add-site
versions: 3.4.0, 3.4.1

# Summary

Add a legacy replication site.

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

3.4.0: c01c696e90722ddf21875f1ca7adc5bd9faa4233784f790f1a5038696a0be2ff
3.4.1: c01c696e90722ddf21875f1ca7adc5bd9faa4233784f790f1a5038696a0be2ff

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_console
concept: cross-cluster-replication
