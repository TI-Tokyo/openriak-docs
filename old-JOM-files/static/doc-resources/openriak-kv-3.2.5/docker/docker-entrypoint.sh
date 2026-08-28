#!/bin/sh

if [ "$1" = 'start-openriak' ]; then
    echo "Starting OpenRiak KV..."
    riak daemon

    echo "Checking OpenRiak KV is reachable:"
    if riak ping | grep -q "pong"; then
        echo "  ✅ OpenRiak is reachable"
    else
        echo "  ❌ OpenRiak is NOT responding"
        exit 1
    fi

    echo "Waiting for OpenRiak KV to start:"

    WAITED=0
    while true; do
        if riak admin services 2>/dev/null | grep -q 'riak_kv'; then
            echo "✅ OpenRiak KV has started!"
            break;
        fi

        echo "  ⏳ Still waiting for OpenRiak KV to start... ($WAITED s)"
        sleep 2
        WAITED=$((WAITED + 2))
    done

    while true; do 
        if riak ping | grep -q "pong"; then
            echo "  ✅ OpenRiak is reachable"
        else
            echo "  ❌ OpenRiak is NOT responding"
            exit 1
        fi
        #echo "Sleeping for 30 seconds..."
        sleep 30; 
    done
else
    exec "$@"
fi
