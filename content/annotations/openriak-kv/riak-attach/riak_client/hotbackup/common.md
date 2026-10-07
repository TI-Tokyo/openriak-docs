# Metadata

command: erlang:riak_client:hotbackup/4
versions: 3.4.0, 3.4.1

# Summary

Request a cluster backup from a supporting backend.

# Description

The backup path must be writable on each participating node. The operation requires backend support; inspect `{ok, Boolean}` and any error before considering a backup successful.

# Arguments

## BackupPath

datatype: filesystem path string
required: true
repeatable: false

### Description

Destination directory on each node, for example `"/tmp/cli-backup"`.

## DefaultNVal

datatype: positive integer
required: true
repeatable: false

### Description

Replication factor used for default coverage.

## PlanNVal

datatype: positive integer
required: true
repeatable: false

### Description

Replication factor used to build the backup coverage plan.

## Client

datatype: riak_client handle
required: true
repeatable: false

### Description

See the shared `Client` argument on the parent module page.

# Errors

## reference-error-1

### Condition

The operation exceeds its configured timeout.

### Description

The API can return `{error, timeout}`. A timed-out write or delete may still complete on replicas.

### Remedy

Check node availability and load. Read back state before retrying a mutation, and choose an appropriate timeout.

# Reviewed against

3.4.0: 815bb88e538201eac507a52916d2b5200f2ba78fcc78c0db3c85617fddb241f8
3.4.1: 85bfc98a2b3d0971b5ef0aed19c3fa89caebaf4d95b4d292e2027dfbc3c0a261

# Tags

feature: client-operations
repository: riak_kv
module: riak_client
concept: data-access
