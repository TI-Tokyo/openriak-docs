# Description

For the named backend `$name`: Approximate byte-size threshold for rolling a Leveled journal file. Used alongside `leveled.journal_objectcount`; randomized limits reduce simultaneous roll events across partitions. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveled
repository: leveled
module: leveled_multi.schema
concept: storage

# Reviewed against

3.4.0: 22b9f68d848520e58e1c456328b113b2fa7b4b5b0fcdf0e4a188e869bd7cc152
3.4.1: 13de45de775019097f35bdca02249cba1e34495f47afd23af67d8c1aca1a6e61
