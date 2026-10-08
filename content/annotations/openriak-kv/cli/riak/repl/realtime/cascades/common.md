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

3.4.0: a89aa527ea4f160ad75d68960f7356a75ba5284d8bdaca0464e451ebb735608a
3.4.1: a89aa527ea4f160ad75d68960f7356a75ba5284d8bdaca0464e451ebb735608a

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_console
concept: cross-cluster-replication
