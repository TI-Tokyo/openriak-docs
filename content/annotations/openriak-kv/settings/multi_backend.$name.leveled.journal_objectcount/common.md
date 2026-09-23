# Description

For the named backend `$name`: Approximate object count at which Leveled rolls a journal file. A file rolls on either the count or byte-size limit; the actual limit is randomized at startup to spread roll events across vnodes. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveled
repository: leveled
module: leveled_multi.schema
concept: storage

# Reviewed against

3.4.0: e96f05e4141b28ea0594a02afe21facc9383c117c74e1fdea846b48b2ffd87ed
3.4.1: 92bab2c0763036a3ba35eb6d6e33ed59a20bf206a54c7b5fa21df9c655252a2e
