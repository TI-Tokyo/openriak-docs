# Description

Approximate byte-size threshold for rolling a Leveled journal file. Used alongside `leveled.journal_objectcount`; randomized limits reduce simultaneous roll events across partitions.

# Tags

feature: leveled
repository: leveled
module: leveled.schema
concept: storage

# Reviewed against

3.4.0: 0885ebf6f962d7f1b9d6d1bb55caa3e3b75dd546c55db0c4da1931842af8eee5
3.4.1: 99d2d7ec7695220a6a4634aeec97a683e4231ef0baafc7ebf30d16987ac57603
