# Metadata

command: erlang:riak:get_app_env/0
versions: 3.4.0, 3.4.1

# Summary

Read application environment and startup arguments.

# Description

With no arguments, returns configured key/value pairs. With a key, returns its value or undefined. The two-argument form supplies a fallback.

# Arguments

## Opt

datatype: atom
required: false
repeatable: false

### Description

Application-environment key as an atom, for example `cli_reference_missing`.

## Default

datatype: Erlang term
required: false
repeatable: false

### Description

Value returned when the key is absent from the application environment and startup arguments.

# Reviewed against

3.4.0: 73d53f71535a04667263c3e97f30f1b9ee696bf53f34d1c7b10240e13c1b48cc
3.4.1: 73d53f71535a04667263c3e97f30f1b9ee696bf53f34d1c7b10240e13c1b48cc

# Tags

feature: client-operations
repository: riak_kv
module: riak
concept: data-access
