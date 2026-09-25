# Description

For the named backend `$name`: Maximum age of a reusable Bitcask key-directory snapshot for folds. Reuse also depends on `bitcask.fold.max_puts`; when either threshold is exceeded, a new fold waits for existing folds before taking a fresh snapshot. `unlimited` disables the age limit. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Notes

The [Cuttlefish mapping](https://github.com/OpenRiak/bitcask/blob/eb7c056b24c0707dd264dfc2037092e7314eeac7/priv/bitcask_multi.schema) declares a duration in milliseconds or the literal atom `unlimited`. It attaches no additional validator; `atom` is the type of the literal, not an unrestricted alternative.

# Tags

feature: bitcask
repository: bitcask
module: bitcask_multi.schema
concept: storage

# Reviewed against

3.4.0: 4b5069558cfbe22e76f00c446242fca6e3fa596989b76d11ff6e4e6b49b17142
3.4.1: 4b5069558cfbe22e76f00c446242fca6e3fa596989b76d11ff6e4e6b49b17142
