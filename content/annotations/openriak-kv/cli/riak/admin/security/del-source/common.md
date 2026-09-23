# Metadata

command: shell:riak admin security del-source
versions: 3.4.0, 3.4.1

# Summary

Delete an authentication source rule.

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

# Results

## outcome

### Description

A successful change removes the source rule from `security print-sources`. The fixture creates the rule before deleting it, then verifies it is absent.

# Reviewed against

3.4.0: 2a4a6416fc6efe1ea48eeeb255b4a196d8f0903111f318acf6386bb1a9d1209c
3.4.1: 2a4a6416fc6efe1ea48eeeb255b4a196d8f0903111f318acf6386bb1a9d1209c

# Tags

feature: security
repository: riak_core
module: riak_core_console
concept: authentication
