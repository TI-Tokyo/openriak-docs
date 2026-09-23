# Metadata

command: shell:riak repl realtime cascades
versions: 3.4.0, 3.4.1

# Summary

Read or change realtime replication cascading.

# Description

Cascading controls whether writes received through replication can be forwarded to other clusters. Omit the argument to read the current setting.

# Arguments

## policy

datatype: policy
required: false
repeatable: false

### Valid values

- always
- never

### Description

Cascading policy.

# Reviewed against

3.4.0: 262c64fca503ca2ebb9851835a34764ac99f4f0ed9f3aa6389eaac9e2233fb34
3.4.1: 262c64fca503ca2ebb9851835a34764ac99f4f0ed9f3aa6389eaac9e2233fb34

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_console
concept: cross-cluster-replication
