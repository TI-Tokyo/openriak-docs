# Description

For the named backend `$name`: Maximum time Bitcask waits while opening or creating its data directory at startup. Consider increasing it only after investigating a backend-open timeout; it does not extend ordinary client request timeouts. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: bitcask
repository: bitcask
module: bitcask_multi.schema
concept: scheduling, storage

# Reviewed against

3.4.0: c1d7d29f1d67af8cb279f47ba459fb78bff5e5a4ed08a3d6933214343d847569
3.4.1: c1d7d29f1d67af8cb279f47ba459fb78bff5e5a4ed08a3d6933214343d847569
