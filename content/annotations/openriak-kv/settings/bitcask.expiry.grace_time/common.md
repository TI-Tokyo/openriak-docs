# Description

Additional delay before expired keys alone trigger a Bitcask merge. Increasing this reduces repeated expiry-driven merges; it delays reclaiming disk space rather than extending the configured retention period.

# Tags

feature: bitcask
repository: bitcask
module: bitcask.schema
concept: retention, storage

# Reviewed against

3.4.0: a823ddab7a936a8addba18753c2593142c81b464be2e5d274bfcef973ac3d749
3.4.1: a823ddab7a936a8addba18753c2593142c81b464be2e5d274bfcef973ac3d749
