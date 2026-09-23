# Description

Maximum time Bitcask waits while opening or creating its data directory at startup. Consider increasing it only after investigating a backend-open timeout; it does not extend ordinary client request timeouts.

# Tags

feature: bitcask
repository: bitcask
module: bitcask.schema
concept: scheduling, storage

# Reviewed against

3.4.0: d87beaf52c345b918dff83797a308eda37e27b8e2a731aa111e1fec3c3d07024
3.4.1: d87beaf52c345b918dff83797a308eda37e27b8e2a731aa111e1fec3c3d07024
