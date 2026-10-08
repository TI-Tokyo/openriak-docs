# Metadata

command: shell:riak admin security revoke
versions: 3.4.0, 3.4.1

# Summary

Revoke permissions on a resource.

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

After `from`, give comma-separated user or group names.

# Reviewed against

3.4.0: 54de2f0369944307c63c05fab90d0c39095ac4df0e02a828a177d0c351d08275
3.4.1: 54de2f0369944307c63c05fab90d0c39095ac4df0e02a828a177d0c351d08275

# Tags

feature: security
repository: riak_core
module: riak_core_console
concept: authentication
