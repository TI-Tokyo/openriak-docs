# Description

For the named backend `$name`: Ledger level to preload into the operating-system page cache. Choose according to available memory and acceptable startup I/O; loading more ledger data can reduce later disk reads. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveled
repository: leveled
module: leveled_multi.schema
concept: memory, storage

# Reviewed against

3.4.0: b26dbb38262d503677457cf1dacf36889cab1eb170fa1cb834dab781cbb35fd1
3.4.1: 408d1ac58c4bf353bebbc442dfc39e33e413bdb336e70ed3126679bfd1dc5b0b
