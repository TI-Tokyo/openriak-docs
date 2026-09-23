# Description

For the named backend `$name`: Interval in seconds between statistics logs from each Leveled monitor. There is one monitor per vnode, so shorter intervals can significantly increase total log volume. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveled
repository: leveled
module: leveled_multi.schema
concept: diagnostics, storage

# Reviewed against

3.4.0: ce2c948f7614c0b3ec7a31cb6b9772207921368647ae930ac863c1891e4e3a8d
3.4.1: bedc458ec011b3e53eff0c5262d588766d2139abeeca6eed0c6a4fbfe49a6e3c
