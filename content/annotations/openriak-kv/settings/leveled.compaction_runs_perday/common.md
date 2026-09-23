# Description

Number of journal-compaction opportunities per vnode per day. Increasing it can reclaim dead space sooner but adds background I/O and CPU work.

# Tags

feature: leveled
repository: leveled
module: leveled.schema
concept: compaction, storage

# Reviewed against

3.4.0: 370a27bb7e172c2cd0a081541c46d1cbf2db46366afbf8a43dc75496aba332ab
3.4.1: 940c54625237c3530c959483fa1edc0e721b2c2e3f642d1acc270be5e56580db
