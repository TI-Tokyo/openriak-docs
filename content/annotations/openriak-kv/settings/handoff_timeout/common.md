# Description

Time in milliseconds to wait for acknowledgement of a handoff batch. Investigate batch size and backend pressure before increasing it; a longer timeout tolerates slow batches but delays failure detection.

# Tags

feature: handoff
repository: riak_core
module: riak_core_handoff_sender
concept: partition-transfer, scheduling

# Reviewed against

3.4.0: fcd214d1eb996b206e6da15c7b165734df7af554c718d37dadb1d9d683ea5134
3.4.1: 3af3087ef84a9fdd99d7a3210836631804aeef4ab7862ce32e9c7e6e79856dce
