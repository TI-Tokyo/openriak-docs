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

3.4.0: aec80191a951f37bcc658fbf7315240fa5ac7a20345f505d81c2a6a0f7a71143
3.4.1: aec80191a951f37bcc658fbf7315240fa5ac7a20345f505d81c2a6a0f7a71143

# Tags

feature: security
repository: riak_core
module: riak_core_console
concept: authentication
