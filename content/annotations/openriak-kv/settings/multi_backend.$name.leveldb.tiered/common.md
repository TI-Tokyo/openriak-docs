# Description

For the named backend `$name`: First LevelDB level placed on the slow storage tier; lower levels use the fast tier. `off` disables tiering. Changing the split does not move existing files automatically, so existing data needs a planned migration. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb_multi.schema
concept: storage

# Reviewed against

3.4.0: 39ef7b8da438683a813b6a795fa59b74d645a3a7962b5914eb279fac41822715
3.4.1: 39ef7b8da438683a813b6a795fa59b74d645a3a7962b5914eb279fac41822715
