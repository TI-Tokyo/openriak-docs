# Description

Upper bound of the randomly selected per-vnode LevelDB write-buffer size. Used with `.write_buffer_size_min` to spread flush activity; larger buffers increase aggregate memory demand across vnodes.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb.schema
concept: memory, storage

# Reviewed against

3.4.0: 7dcc3fd5ccc94828aa82291e7fc32dd1c98494dc27a5edd6c4f7812dbde70411
3.4.1: 7dcc3fd5ccc94828aa82291e7fc32dd1c98494dc27a5edd6c4f7812dbde70411
