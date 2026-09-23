# Description

For the named backend `$name`: Maximum expected lifetime, in seconds, of long Leveled fold snapshots. A fold exceeding this time may fail when its snapshot is released and old files become eligible for deletion. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveled
repository: leveled
module: leveled_multi.schema
concept: scheduling, storage

# Reviewed against

3.4.0: e64aa4edab748e1bf6a81d30a32388b88cde211f06d536adf16db0842b3c4f9d
3.4.1: 84a9dd7bf4689563d8aa92cd3990caa728d3d23e89c134c4ef6c82f7031bca5c
