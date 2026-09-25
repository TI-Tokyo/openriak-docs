# Description

For the named backend `$name`: Percentage of requests sampled by Leveled statistics monitoring. Higher sampling improves coverage but adds monitor messages; the monitor has no flow control to protect it from excessive sampling traffic. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Constraints

- Use an integer percentage from 0 through 100 inclusive.

# Tags

feature: leveled
repository: leveled
module: leveled_multi.schema
concept: diagnostics, storage

# Reviewed against

3.4.0: f25f4ff2dd97ddb13acacab43c28b0fad0fbde13e32ba058a73a20b478e531a8
3.4.1: df61a1265711c8e9c9bbc7dd4a972d2bb89eec229e62533c2e3c39739b3ddac0
