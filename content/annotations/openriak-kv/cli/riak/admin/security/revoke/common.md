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

3.4.0: 558f543c71976deffae8ba5a429cea82b30e8dd85eb2737b13480bff4472eb91
3.4.1: 558f543c71976deffae8ba5a429cea82b30e8dd85eb2737b13480bff4472eb91
