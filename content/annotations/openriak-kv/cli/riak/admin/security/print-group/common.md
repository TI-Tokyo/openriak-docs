# Metadata

command: shell:riak admin security print-group
versions: 3.4.0, 3.4.1

# Summary

Inspect a security group.

# Description

Displays the role’s configuration or grants. Review this together with authentication source rules when diagnosing access.

# Arguments

## group

datatype: group name
required: true
repeatable: false

### Description

Security group name, for example `cli_readers`.

# Reviewed against

3.4.0: af16424d874b6f908155a9843152e3372930d62262188fcc37d1f27e86713b05
3.4.1: af16424d874b6f908155a9843152e3372930d62262188fcc37d1f27e86713b05

# Tags

feature: security
repository: riak_core
module: riak_core_console
concept: authentication
