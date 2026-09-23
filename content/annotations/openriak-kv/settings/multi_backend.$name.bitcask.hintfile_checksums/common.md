# Description

For the named backend `$name`: Choose whether Bitcask hint files must contain a CRC checksum. `allow_missing` accepts older hint files without checksums; requiring checksums strengthens validation but removes that compatibility allowance. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: bitcask
repository: bitcask
module: bitcask_multi.schema
concept: storage

# Reviewed against

3.4.0: 9ac37d512c4ed27aa800d1008a924ae32536213a601b0782d91ba43e3cfe556d
3.4.1: 9ac37d512c4ed27aa800d1008a924ae32536213a601b0782d91ba43e3cfe556d
