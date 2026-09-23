# Description

Maximum age of a reusable Bitcask key-directory snapshot for folds. Reuse also depends on `bitcask.fold.max_puts`; when either threshold is exceeded, a new fold waits for existing folds before taking a fresh snapshot. `unlimited` disables the age limit.

# Tags

feature: bitcask
repository: bitcask
module: bitcask.schema
concept: storage

# Reviewed against

3.4.0: 3b467348c28114db22e07a67e92573bf4a955f7bef584b179bf951361b628acc
3.4.1: 3b467348c28114db22e07a67e92573bf4a955f7bef584b179bf951361b628acc
