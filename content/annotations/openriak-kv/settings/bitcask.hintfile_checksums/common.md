# Description

Choose whether Bitcask hint files must contain a CRC checksum. `allow_missing` accepts older hint files without checksums; requiring checksums strengthens validation but removes that compatibility allowance.

# Tags

feature: bitcask
repository: bitcask
module: bitcask, bitcask_fileops
concept: storage

# Reviewed against

3.4.0: cbec5171d7eea1c715678ab83889c69a809b4879e530e03dc9af0ee2dce7fb62
3.4.1: cbec5171d7eea1c715678ab83889c69a809b4879e530e03dc9af0ee2dce7fb62
