# Metadata

command: shell:riak admin cluster-info
versions: 3.4.0, 3.4.1

# Summary

Write a diagnostic report for selected cluster nodes.

# Description

The report gathers cluster and application state. Choose a writable destination and include only the nodes needed for the investigation.

# Arguments

## output_file

datatype: filesystem path
required: true
repeatable: false

### Description

Output report path, for example `/tmp/cli-cluster-info.txt`.

## node

datatype: node selector
required: false
repeatable: true

### Description

One or more full node names or `local`.

# Results

## outcome

### Description

A successful invocation writes a diagnostic report to the requested file. The test also checks that the report file is nonempty.

# Reviewed against

3.4.0: cec9651de46029c224a283ea21109da93152bd960cd27b60976cb56eeef734c3
3.4.1: cec9651de46029c224a283ea21109da93152bd960cd27b60976cb56eeef734c3

# Tags

feature: cluster-management
repository: riak_kv
module: riak_kv_console
concept: partition-placement
