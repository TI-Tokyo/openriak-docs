# Description

For the named backend `$name`: Maximum number of updates allowed while reusing a Bitcask fold snapshot. Used with `bitcask.fold.max_age` to decide whether a fold can reuse the key directory or must wait for a fresh snapshot. `unlimited` disables this update-count limit. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: bitcask
repository: bitcask
module: bitcask_multi.schema
concept: storage

# Reviewed against

3.4.0: ecf1c046af11104243ae12cbf7da1a61ccd692bcc49ba440975b0531b6db382f
3.4.1: ecf1c046af11104243ae12cbf7da1a61ccd692bcc49ba440975b0531b6db382f
