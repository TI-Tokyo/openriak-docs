# Description

Choose when journal objects are compressed: on receipt or during compaction. Deferring compression to compaction avoids immediate compression work on incoming writes; ledger compression has its own controls.

# Tags

feature: leveled
repository: leveled
module: leveled.schema
concept: compression, storage

# Reviewed against

3.4.0: 1f95b531c08fdcc6ab78f9f211009c48ae9aaefe60ba54341ac0128f6a29db25
3.4.1: 35826ee593f863c1aa1022c0827b7cc65ac576df9e54537433658a13f7e87056
