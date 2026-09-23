# Description

For the named backend `$name`: Key-count capacity of the Leveled Penciller's memory cache. This governs ledger-side buffering and is separate from the Bookie cache configured by `leveled.cache_size`. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveled
repository: leveled
module: leveled_multi.schema
concept: memory, storage

# Reviewed against

3.4.0: e0f480fa9838a0a6008bba7e51ebe0fb102ee0af97fd6b6fc656fdc15b8a177e
3.4.1: 646a7996fb769c14ca57d612b58cebfeb0dd8456bb7e8c020ca81840af6513d6
