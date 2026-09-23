# Description

Size threshold for rolling a Bitcask data file. A write that takes the current file beyond the threshold causes subsequent writes to use a new file; the threshold is not a total database-size limit.

# Tags

feature: bitcask
repository: bitcask
module: bitcask.schema
concept: storage

# Reviewed against

3.4.0: 46c0512fc63407e8a1bfd3daf4e1b43aff3dc7cee23590035cabbced2e6e27f8
3.4.1: 46c0512fc63407e8a1bfd3daf4e1b43aff3dc7cee23590035cabbced2e6e27f8
