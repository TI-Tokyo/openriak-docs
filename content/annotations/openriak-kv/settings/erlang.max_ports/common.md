# Description

Maximum number of Erlang ports, including sockets and file-related ports. This is a VM resource limit; the operating system's file-descriptor limit must also accommodate the expected workload.

# Tags

feature: erlang-runtime
repository: cuttlefish
module: erlang_vm.schema
concept: runtime

# Reviewed against

3.4.0: 22fababfbeed96d0ef6fb177328f1d6fffc1b424fa3c705e9960c6934332e679
3.4.1: 22fababfbeed96d0ef6fb177328f1d6fffc1b424fa3c705e9960c6934332e679

# Application name

vm_args.+Q
