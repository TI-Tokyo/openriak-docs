# Description

Compression codec used by Leveled. `native` uses Erlang's built-in zlib term compression; `lz4` and `zstd` use their supported codec implementations. Ledger compression can be selected separately.

# Tags

feature: leveled
repository: leveled
module: leveled.schema
concept: compression, storage

# Reviewed against

3.4.0: b5e05366cfe53e21d133d8fb6b401c421737e436a76f25dd5b1127f287d7882b
3.4.1: 5cf1d4837c3e342dc23195dbcd64186ce0ab18c776683525e0f069e90840e08a
