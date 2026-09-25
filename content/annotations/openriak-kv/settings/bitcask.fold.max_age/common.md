# Description

Maximum age of a reusable Bitcask key-directory snapshot for folds. Reuse also depends on `bitcask.fold.max_puts`; when either threshold is exceeded, a new fold waits for existing folds before taking a fresh snapshot. `unlimited` disables the age limit.

# Notes

The [Cuttlefish mapping](https://github.com/OpenRiak/bitcask/blob/eb7c056b24c0707dd264dfc2037092e7314eeac7/priv/bitcask.schema) declares a duration in milliseconds or the literal atom `unlimited`. It attaches no additional validator; `atom` is the type of the literal, not an unrestricted alternative.

# Tags

feature: bitcask
repository: bitcask
module: bitcask.schema
concept: storage

# Reviewed against

3.4.0: 3b467348c28114db22e07a67e92573bf4a955f7bef584b179bf951361b628acc
3.4.1: 3b467348c28114db22e07a67e92573bf4a955f7bef584b179bf951361b628acc
