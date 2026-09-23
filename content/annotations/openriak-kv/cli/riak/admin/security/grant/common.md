# Metadata

command: shell:riak admin security grant
versions: 3.4.0, 3.4.1

# Summary

Grant permissions on a resource.

# Description

Use the narrowest appropriate resource scope. Review effective permissions with print-grants after changing a grant.

# Arguments

## permissions

datatype: permission list
required: true
repeatable: false

### Description

Comma-separated permission names, for example `riak_kv.get,riak_kv.list_keys`.

## scope

datatype: resource scope
required: true
repeatable: false

### Description

After `on`, specify `any`, a bucket type, or a bucket type followed by a bucket name. For example, `on default cli_reference`.

## users

datatype: role list
required: true
repeatable: false

### Description

After `to`, give comma-separated user or group names.

# Reviewed against

3.4.0: 9bd3f7323072139b9162120d40e10d4eb160f25c6112d77a00968e6cc9285559
3.4.1: 9bd3f7323072139b9162120d40e10d4eb160f25c6112d77a00968e6cc9285559

# Tags

feature: security
repository: riak_core
module: riak_core_console
concept: authentication
