# Description

Enable kernel polling in the Erlang emulator when supported. This controls VM event polling rather than Riak request concurrency; unsupported runtimes may report a startup warning.

# Tags

feature: erlang-runtime
repository: cuttlefish
module: erlang_vm.schema
concept: runtime

# Reviewed against

3.4.0: 96c77487f0aba2d00c6d3a95bef58e2a6bedb09405b6ef0b6a11148c4a53cda2
3.4.1: 96c77487f0aba2d00c6d3a95bef58e2a6bedb09405b6ef0b6a11148c4a53cda2
