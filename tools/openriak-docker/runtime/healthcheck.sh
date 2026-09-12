#!/bin/sh
set -eu

if ! pgrep -x beam.smp >/dev/null 2>&1
then
    echo "OpenRiak healthcheck failed: beam.smp is not running"
    exit 1
fi

ping_output=$(/usr/sbin/riak ping 2>/dev/null || true)
if [ "$ping_output" != "pong" ]
then
    echo "OpenRiak healthcheck failed: riak ping did not return pong"
    exit 1
fi

echo "OpenRiak healthcheck passed: BEAM is running and riak ping returned pong"
