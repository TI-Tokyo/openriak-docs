# Metadata

command: shell:riak repl clusterstats
versions: 3.4.0, 3.4.1

# Summary

Read statistics for replication control connections.

# Description

With no selector, report all known connections. Supply a remote endpoint or protocol identifier to narrow the report.

# Arguments

## connection

datatype: endpoint or protocol identifier
required: false
repeatable: false

### Description

Remote IP:port or protocol identifier. Omit to inspect all connections.

# Options

## -port

omit: true

# Reviewed against

3.4.0: 65b6c86b37b61aa6d7f2da2e9492a771a43ddee258b9dabe02cb3238136d16cd
3.4.1: 9fd03f5710600bf38282594e2e006eae5f71b5db2f1c0020712fdb7cd72ad17c

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_console
concept: cross-cluster-replication, diagnostics
