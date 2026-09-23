# Description

Number of normal scheduler threads created by the Erlang VM. `erlang.schedulers.online` controls how many start online. Zero uses the runtime default; negative values offset the detected processor count.

# Tags

feature: erlang-runtime
repository: cuttlefish
module: erlang_vm.schema
concept: concurrency, runtime

# Reviewed against

3.4.0: 45603d9e1b0a94ffc58ef36956d41a374d9e334ff011f2978c92bfbe877db418
3.4.1: 45603d9e1b0a94ffc58ef36956d41a374d9e334ff011f2978c92bfbe877db418
