# Metadata

command: shell:riak admin security enable
versions: 3.4.0, 3.4.1

# Summary

Enable Riak security.

# Description

Changes the security enforcement state. Configure users, authentication sources and grants before enabling security so clients can authenticate and retain the intended access.

# Arguments

# Examples

## shell-riak-admin-security-enable:change-enforcement

### Description

Change the security state on this node.

# Reviewed against

3.4.0: 7c4eba010f2df357785c2b63d2ea73126cf0bf00de0b77483883faa9a1b3af1a
3.4.1: dc04603deb382c27eee4b35e9cd5bd6c6dee5b2ecfe4d97de65cfcc55cbac13c

# Tags

feature: security
repository: riak_core
module: riak_core_console
concept: authentication
