# Description

Dead-data size in any one Bitcask file that triggers a merge attempt. Lower values trigger earlier, more frequent merges; the separate merge thresholds determine which files participate.

# Tags

feature: bitcask
repository: bitcask
module: bitcask.schema
concept: compaction, storage

# Reviewed against

3.4.0: 1332910b4b35242369b2cd80858cabc53ea1bc5e04369cceb9ffddc8bb9ad59b
3.4.1: 1332910b4b35242369b2cd80858cabc53ea1bc5e04369cceb9ffddc8bb9ad59b
