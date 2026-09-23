# Description

Approximate object count at which Leveled rolls a journal file. A file rolls on either the count or byte-size limit; the actual limit is randomized at startup to spread roll events across vnodes.

# Tags

feature: leveled
repository: leveled
module: leveled.schema
concept: storage

# Reviewed against

3.4.0: bc78b63be59c16d98573e5f3328c01eb626ccd8e7b2db80b1a5e706823ccd6f9
3.4.1: 21753f736a5d1aff3b24d39d4cf75aa7b0d5b870fefe9a040db553816513901b
