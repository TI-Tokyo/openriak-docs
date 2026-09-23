# Description

Multiplier of the Bookie cache size at which new PUTs request a slow-offer pause. Used with `leveled.cache_size` to apply write backpressure when the cache is not draining quickly enough.

# Tags

feature: leveled
repository: leveled
module: leveled.schema
concept: memory, storage

# Reviewed against

3.4.0: 77b025439f65a58d50e0ebc96e1439e969a711c80e1d4869e669b033c5e3147a
3.4.1: 060a7ba04d3faf6b32ed9c5ce7c76becc80d571877d5b735b54791b988b919a3
