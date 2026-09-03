# syntax=docker/dockerfile:1.7
# Generated and tested by tools/openriak-docker/openriak-docker. Do not edit by hand.
FROM --platform=linux/amd64 alpine:3.21@sha256:48b0309ca019d89d40f670aa1bc06e426dc0931948452e8491e3d65087abc07d

# -----------------------------------------------------------------------------
# OpenRiak KV default settings
# Override any value with `docker run --env NAME=value` or Compose `environment`.
# -----------------------------------------------------------------------------
ENV RIAK_NODE_HOST=""
ENV RIAK_NODE_NAME=""
ENV RIAK_RING_SIZE="8"
ENV RIAK_STORAGE_BACKEND="leveled"
ENV RIAK_ANTI_ENTROPY="passive"
ENV RIAK_TICTACAAE_ACTIVE="active"
ENV RIAK_TICTACAAE_STOREHEADS="enabled"
ENV RIAK_HTTP_LISTENER="0.0.0.0:8098"
ENV RIAK_PB_LISTENER="0.0.0.0:8087"
ENV RIAK_NOFILE_LIMIT="100000"
ENV RIAK_INIT_ONLY="0"
ENV RIAK_STARTUP_POLL_SECONDS="1"
ENV RIAK_SHUTDOWN_POLL_SECONDS="1"
ENV RIAK_MONITOR_INTERVAL_SECONDS="10"

ADD --checksum=sha256:140f1decb585e5855990c140b58afcb2ba3629e5dc65fffab8d0eaaa0621cc69 https://files.tiot.jp/alpine/v3.21/main/x86_64/riak-3.4.0.24-r1.apk /tmp/riak-3.4.0.24-r1.apk
RUN <<'OPENRIAK_PACKAGE_INSTALL'
set -eu
apk add --no-cache bash ca-certificates curl su-exec
apk add --no-cache --allow-untrusted /tmp/riak-3.4.0.24-r1.apk
rm -f /tmp/riak-3.4.0.24-r1.apk
OPENRIAK_PACKAGE_INSTALL

RUN <<'OPENRIAK_IMAGE_SETUP'
set -eu
if ! getent group riak >/dev/null 2>&1
then
    addgroup -S riak
fi
if ! id riak >/dev/null 2>&1
then
    adduser -S -D -H -h /var/lib/riak -s /sbin/nologin -G riak riak
fi
test -x /usr/sbin/riak
id riak
mkdir -p /opt/openriak-defaults/etc-riak /var/lib/riak /var/log/riak /run/riak /usr/lib/riak/log
cp -a /etc/riak/. /opt/openriak-defaults/etc-riak/
chown -R riak:riak /var/lib/riak /var/log/riak /run/riak /usr/lib/riak/log
OPENRIAK_IMAGE_SETUP

COPY <<'OPENRIAK_ENTRYPOINT' /usr/local/bin/openriak-entrypoint
#!/bin/sh
set -eu

config_dir=/etc/riak
data_dir=/var/lib/riak
log_dir=/var/log/riak
defaults_dir=/opt/openriak-defaults/etc-riak

log() {
    printf '%s [openriak-entrypoint] %s
' "$(date -u +'%Y-%m-%dT%H:%M:%SZ')" "$*"
}

one_line() {
    tr '
' ' ' | sed 's/[[:space:]][[:space:]]*/ /g; s/[[:space:]]$//'
}

riak_command() {
    if command -v su-exec >/dev/null 2>&1
    then
        su-exec riak /usr/sbin/riak "$@"
        return
    fi
    if command -v runuser >/dev/null 2>&1
    then
        runuser -u riak -- /usr/sbin/riak "$@"
        return
    fi
    su -s /bin/sh riak -c "/usr/sbin/riak $*"
}

beam_running() {
    pgrep -x beam.smp >/dev/null 2>&1
}

shutdown() {
    shutdown_signal=$1
    trap - HUP INT TERM
    log "shutdown: received ${shutdown_signal}"
    if beam_running
    then
        log "shutdown: requesting OpenRiak stop"
        if riak_command stop
        then
            log "shutdown: OpenRiak accepted the stop request"
        else
            log "shutdown: OpenRiak stop command returned an error"
        fi
    else
        log "shutdown: BEAM is already stopped"
    fi
    shutdown_attempt=0
    while beam_running
    do
        shutdown_attempt=$((shutdown_attempt + 1))
        log "shutdown: waiting for BEAM to stop (attempt ${shutdown_attempt})"
        sleep "${RIAK_SHUTDOWN_POLL_SECONDS:-1}"
    done
    log "shutdown: BEAM stopped; container is exiting"
    exit 0
}

trap 'shutdown SIGHUP' HUP
trap 'shutdown SIGINT' INT
trap 'shutdown SIGTERM' TERM

log "configuration: preparing mounted directories"
mkdir -p "$config_dir" "$data_dir" "$log_dir" /run/riak
if [ ! -s "$config_dir/riak.conf" ]
then
    log "configuration: seeding /etc/riak from packaged defaults"
    cp -a "$defaults_dir/." "$config_dir/"
else
    log "configuration: using existing /etc/riak/riak.conf"
fi

set_setting() {
    key=$1
    value=$2
    escaped_key=$(printf '%s' "$key" | sed 's/[.[\*^$()+?{|]/\\&/g')
    if grep -Eq "^[[:space:]]*${escaped_key}[[:space:]]*=" "$config_dir/riak.conf"
    then
        sed -i -E "s|^[[:space:]]*${escaped_key}[[:space:]]*=.*$|${key} = ${value}|" "$config_dir/riak.conf"
    else
        printf '
%s = %s
' "$key" "$value" >> "$config_dir/riak.conf"
    fi
    log "configuration: ${key} = ${value}"
}

node_host=${RIAK_NODE_HOST:-$(hostname)}
set_setting nodename "${RIAK_NODE_NAME:-riak@$node_host}"
set_setting ring_size "$RIAK_RING_SIZE"
set_setting storage_backend "$RIAK_STORAGE_BACKEND"
set_setting anti_entropy "$RIAK_ANTI_ENTROPY"
set_setting tictacaae_active "$RIAK_TICTACAAE_ACTIVE"
set_setting tictacaae_storeheads "$RIAK_TICTACAAE_STOREHEADS"
set_setting listener.http.internal "$RIAK_HTTP_LISTENER"
set_setting listener.protobuf.internal "$RIAK_PB_LISTENER"

chown -R riak:riak "$config_dir" "$data_dir" "$log_dir" /run/riak
if [ "${RIAK_INIT_ONLY:-0}" = "1" ]
then
    log "initialization: volume setup complete; RIAK_INIT_ONLY requested"
    exit 0
fi

ulimit -n "${RIAK_NOFILE_LIMIT:-100000}"
log "startup: starting OpenRiak as a daemon"
if riak_command daemon
then
    log "startup: daemon command completed"
else
    log "startup: daemon command failed"
    exit 1
fi

startup_attempt=0
log "startup: waiting for BEAM and riak ping"
while :
do
    startup_attempt=$((startup_attempt + 1))
    beam_status=stopped
    if beam_running
    then
        beam_status=running
    fi
    ping_output=$(riak_command ping 2>&1 || true)
    ping_value=$(printf '%s' "$ping_output" | tr -d '\r\n')
    if [ "$beam_status" = "running" ] && [ "$ping_value" = "pong" ]
    then
        log "startup: BEAM is running and riak ping returned pong"
        break
    fi
    ping_summary=$(printf '%s' "$ping_output" | one_line)
    log "startup: waiting for BEAM/ping (attempt ${startup_attempt}, beam=${beam_status}, ping=${ping_summary:-no-response})"
    sleep "${RIAK_STARTUP_POLL_SECONDS:-1}"
done

service_attempt=0
log "startup: waiting for the riak_kv service"
while :
do
    service_attempt=$((service_attempt + 1))
    services_output=$(riak_command admin services 2>&1 || true)
    if printf '%s
' "$services_output" | grep -Fq 'riak_kv'
    then
        services_summary=$(printf '%s' "$services_output" | one_line)
        log "startup: riak_kv service is up (${services_summary})"
        break
    fi
    services_summary=$(printf '%s' "$services_output" | one_line)
    log "startup: waiting for riak_kv (attempt ${service_attempt}, services=${services_summary:-no-response})"
    sleep "${RIAK_STARTUP_POLL_SECONDS:-1}"
done

transfer_attempt=0
log "startup: waiting for Riak transfers to complete"
while :
do
    transfer_attempt=$((transfer_attempt + 1))
    transfers_output=$(riak_command admin transfers 2>&1 || true)
    if printf '%s
' "$transfers_output" | grep -Eq 'No transfers (active|in progress)'
    then
        transfers_summary=$(printf '%s' "$transfers_output" | one_line)
        log "startup: transfers complete (${transfers_summary})"
        break
    fi
    transfers_summary=$(printf '%s' "$transfers_output" | one_line)
    log "startup: waiting for transfers (attempt ${transfer_attempt}, transfers=${transfers_summary:-no-response})"
    sleep "${RIAK_STARTUP_POLL_SECONDS:-1}"
done

log "startup: OpenRiak is ready"
while :
do
    log "monitor: sleeping for ${RIAK_MONITOR_INTERVAL_SECONDS:-10}s"
    sleep "${RIAK_MONITOR_INTERVAL_SECONDS:-10}"
    if beam_running
    then
        log "monitor: BEAM is running"
    else
        log "monitor: BEAM stopped unexpectedly; container is exiting"
        exit 1
    fi
done
OPENRIAK_ENTRYPOINT

COPY <<'OPENRIAK_HEALTHCHECK' /usr/local/bin/openriak-healthcheck
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
OPENRIAK_HEALTHCHECK

RUN <<'OPENRIAK_SCRIPT_SETUP'
set -eu
chmod 0755 /usr/local/bin/openriak-entrypoint
chmod 0755 /usr/local/bin/openriak-healthcheck
OPENRIAK_SCRIPT_SETUP

VOLUME ["/etc/riak"]
VOLUME ["/var/lib/riak"]
VOLUME ["/var/log/riak"]
EXPOSE 8087
EXPOSE 8098
HEALTHCHECK --interval=10s --timeout=10s --start-period=60s --retries=3 CMD ["/usr/local/bin/openriak-healthcheck"]
STOPSIGNAL SIGTERM
ENTRYPOINT ["/usr/local/bin/openriak-entrypoint"]
