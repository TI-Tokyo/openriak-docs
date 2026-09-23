# Description

For the named backend `$name`: Optional codec selection specifically for the Leveled ledger. `as_store` follows `leveled.compression_method`; other supported values let the ledger use a different codec or no compression. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveled, multi-backend
repository: leveled
module: leveled_multi.schema
concept: compression, storage

# Reviewed against

3.4.0: e0355e7019760cc7cebde400fb51aecad294457e58481ae4f66fb546be2fdef8
3.4.1: 3a482219fba7dad3746e01ada81ce5b87a18d4dbc8c17348ce88ad939f6df674
