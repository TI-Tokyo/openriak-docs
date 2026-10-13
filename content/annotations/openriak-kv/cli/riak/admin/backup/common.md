# Metadata

command: shell:riak admin backup
versions: 3.4.0, 3.4.1

# Summary

Export objects with the legacy backup tool.

# Description

This starts a separate Erlang helper against the named node. Review backend and archive compatibility before using it; use a tested backup/restore procedure for production.

# Arguments

## node

datatype: Erlang node name
required: true
repeatable: false

### Description

Full Erlang node name, for example `openriak-kv@node1.test`.

## cookie

datatype: cookie text
required: true
repeatable: false

### Description

Distribution cookie matching the destination node. Prefer invoking from a protected administrative environment.

## filename

datatype: filesystem path
required: true
repeatable: false

### Description

Backup archive path, readable for restore and writable for backup.

## scope

datatype: scope
required: true
repeatable: false

### Valid values

- node
- all

### Description

Choose the named node or all nodes. The launcher requires this argument despite brackets in its usage text.

# Examples

## reference-example-1

title: A prepared archive operation

### Invocation

```sh
riak admin backup openriak-kv@node1.test "$RIAK_COOKIE" /path/to/backup.archive all
```

### Description

Set RIAK_COOKIE in your protected administrative environment and choose the intended archive path.

### Expected output

Archive progress or an error from node connectivity, archive I/O or backend compatibility.

# Results

## reference-result-1

### Description

A successful helper operation reports its result and returns. Verify archive integrity and test recovery separately before relying on a backup.

# Reviewed against

3.4.0: f8619d32ff31524f3ba586451c4f33658860706ddda813963cc00a8dddb60436
3.4.1: 4fd620614d98a7052699551e7483315657029276ddd680f550d2f698c2b8a445

# Tags

feature: node-operations
repository: riak
module: riak-admin
concept: node-lifecycle
