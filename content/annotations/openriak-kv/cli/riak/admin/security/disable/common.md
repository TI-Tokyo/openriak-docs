# Metadata

command: shell:riak admin security disable
versions: 3.4.0, 3.4.1

# Summary

Disable Riak security.

# Description

Changes the security enforcement state. Configure users, authentication sources and grants before enabling security so clients can authenticate and retain the intended access.

# Arguments

# Examples

## shell-riak-admin-security-disable:change-enforcement

### Description

Change the security state on this node.

# Reviewed against

3.4.0: 5d0cc4c587fd84ac50bc10607c42038c3f2ba07122a2c62dbcc09c7d56a11415
3.4.1: 5d0cc4c587fd84ac50bc10607c42038c3f2ba07122a2c62dbcc09c7d56a11415

# Tags

feature: security
repository: riak_core
module: riak_core_console
concept: authentication
