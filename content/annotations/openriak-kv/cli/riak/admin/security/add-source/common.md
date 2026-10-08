# Metadata

command: shell:riak admin security add-source
versions: 3.4.0, 3.4.1

# Summary

Add an authentication source rule.

# Description

Source rules match users and client networks. They select authentication; data access still requires grants.

# Arguments

## users

datatype: user list or all
required: true
repeatable: false

### Description

Comma-separated user names, or `all` to match every user. For example, `cli_reader`.

## CIDR

datatype: IPv4 or IPv6 CIDR
required: true
repeatable: false

### Description

Client network in CIDR notation, for example `127.0.0.1/32`.

## source

datatype: authentication method
required: true
repeatable: false

### Description

Authentication mechanism, such as `password`, `certificate` or `trust`. Choose a method appropriate to the transport and deployment.

## option=value

datatype: key=value assignment
required: false
repeatable: true

### Description

Authentication-method-specific options. Only supply options supported by that mechanism.

# Results

## outcome

### Description

A successful change adds the source rule shown by `security print-sources`. The example preserves the intended CIDR and verifies the resulting rule.

# Reviewed against

3.4.0: fa1e9112677f54d9695e1cf1f46f9d1f81a3bf3155bfae1c10aa7f515e8e7a99
3.4.1: fa1e9112677f54d9695e1cf1f46f9d1f81a3bf3155bfae1c10aa7f515e8e7a99

# Tags

feature: security
repository: riak_core
module: riak_core_console
concept: authentication
