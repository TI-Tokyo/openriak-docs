# Description

Time in milliseconds that a vnode pauses after a backend write requests backpressure. Currently used by Leveled; a longer pause gives its backend more time to drain pending work but delays new vnode work.

# Tags

feature: leveled
repository: riak_kv
module: riak_kv_leveled_backend
concept: storage

# Reviewed against

3.4.0: 98d37421ae5cf20504cd2c1604253a7d0b058f029f978cbe47017eca3c5092bc
3.4.1: 9f52e1adb62fc43fd9d2c666d8b9415a86d5f2b139e8281c831cdf0613ab97da
