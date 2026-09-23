# Description

For the named backend `$name`: Compression codec used by Leveled. `native` uses Erlang's built-in zlib term compression; `lz4` and `zstd` use their supported codec implementations. Ledger compression can be selected separately. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveled
repository: leveled
module: leveled_multi.schema
concept: compression, storage

# Reviewed against

3.4.0: 946f31dd0c918ca7383e58800a2e56fa5114e3083869750a76a11003e4f94e68
3.4.1: ff9c6c93bb1f1b6f9778ce7b43dea206146fcb6eb051c4c3381a5337bc574fe3
