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
ENV OPENRIAK_CLUSTER_MODE="single"
ENV OPENRIAK_CLUSTER_CONTROL_DIR="/var/lib/openriak-cluster-control"
ENV OPENRIAK_CLUSTER_POLL_SECONDS="1"
ENV OPENRIAK_CLUSTER_WAIT_SECONDS="300"
ENV role=""

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
control_dir=${OPENRIAK_CLUSTER_CONTROL_DIR:-/var/lib/openriak-cluster-control}

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

riak_admin_command() {
    admin_vmargs=
    for admin_vmargs_candidate in "$data_dir"/generated.conf/vm.*.args
    do
        [ -r "$admin_vmargs_candidate" ] || continue
        admin_vmargs=$admin_vmargs_candidate
    done
    if [ -z "$admin_vmargs" ]
    then
        log "cluster: generated VM arguments are not available for riak-admin"
        return 1
    fi
    if command -v su-exec >/dev/null 2>&1
    then
        VMARGS_PATH="$admin_vmargs" su-exec riak /usr/lib/riak/bin/riak-admin "$@"
        return
    fi
    if command -v runuser >/dev/null 2>&1
    then
        VMARGS_PATH="$admin_vmargs" runuser -u riak -- /usr/lib/riak/bin/riak-admin "$@"
        return
    fi
    su -s /bin/sh riak -c "VMARGS_PATH='$admin_vmargs' /usr/lib/riak/bin/riak-admin $*"
}

log_cluster_command_output() {
    command_name=$1
    command_output=$2
    printf '%s
' "$command_output" | while IFS= read -r command_line
    do
        log "cluster: ${command_name}: ${command_line}"
    done
}

join_output_is_successful() {
    printf '%s
' "$1" | grep -Eq 'Success: staged join request|already (a )?member'
}

plan_output_is_successful() {
    printf '%s
' "$1" | grep -Eq 'Staged Changes|To commit these changes'
}

commit_output_is_successful() {
    printf '%s
' "$1" | grep -Eiq 'cluster changes committed'
}

beam_running() {
    pgrep -x beam.smp >/dev/null 2>&1
}

ping_works() {
    ping_output=$(riak_command ping 2>&1 || true)
    ping_value=$(printf '%s' "$ping_output" | tr -d '\r\n')
    [ "$ping_value" = "pong" ]
}

validate_nodename() {
    printf '%s
' "$1" | grep -Eq '^riak@[A-Za-z0-9][A-Za-z0-9._:-]*$'
}

atomic_control_file() {
    control_path=$1
    control_node=$2
    control_suffix=$3
    control_temporary="${control_path}.tmp.$$"
    printf '%s
%s
' "$control_node" "$control_suffix" > "$control_temporary"
    mv -f "$control_temporary" "$control_path"
}

clean_owned_control_files() {
    for owned_file in "$control_dir/${riak_node_name}-"*
    do
        [ -e "$owned_file" ] || continue
        rm -f "$owned_file"
        log "cluster: removed stale owned control file $(basename "$owned_file")"
    done
}

cluster_member() {
    member_output=$(riak_command admin member-status 2>&1 || true)
    member_count=$(printf '%s
' "$member_output" | grep -Ec '^[[:space:]]*(valid|joining|leaving|exiting|down)[[:space:]]' || true)
    [ "$member_count" -gt 1 ]
}

wait_for_ring() {
    ring_attempt=0
    log "cluster: waiting for the ring to become ready"
    while :
    do
        ring_attempt=$((ring_attempt + 1))
        ring_output=$(riak_command admin ringready 2>&1 || true)
        if printf '%s
' "$ring_output" | grep -Eq '(^|[[:space:]])TRUE([[:space:]]|$)'
        then
            ring_summary=$(printf '%s' "$ring_output" | one_line)
            log "cluster: ring is ready (${ring_summary})"
            return
        fi
        ring_summary=$(printf '%s' "$ring_output" | one_line)
        log "cluster: waiting for ring readiness (attempt ${ring_attempt}, status=${ring_summary:-no-response})"
        sleep "${RIAK_STARTUP_POLL_SECONDS:-1}"
    done
}

wait_for_transfers() {
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
            return
        fi
        transfers_summary=$(printf '%s' "$transfers_output" | one_line)
        log "startup: waiting for transfers (attempt ${transfer_attempt}, transfers=${transfers_summary:-no-response})"
        sleep "${RIAK_STARTUP_POLL_SECONDS:-1}"
    done
}

cluster_failure_exists() {
    failure_suffix=$1
    for failure_file in "$control_dir/"*-"${failure_suffix}"-failed
    do
        [ -e "$failure_file" ] || continue
        return 0
    done
    return 1
}

stop_with_error() {
    failure_message=$1
    log "cluster: failure: ${failure_message}"
    if beam_running
    then
        riak_command stop || true
        while beam_running
        do
            log "cluster: waiting for BEAM to stop after failure"
            sleep "${RIAK_SHUTDOWN_POLL_SECONDS:-1}"
        done
    fi
    exit 1
}

publish_failure() {
    failure_suffix=$1
    failure_message=$2
    atomic_control_file "$control_dir/${riak_node_name}-${failure_suffix}-failed" "$riak_node_name" "$failure_suffix"
    stop_with_error "$failure_message"
}

monitor_node() {
    log "startup: OpenRiak is ready"
    while :
    do
        log "monitor: sleeping for ${RIAK_MONITOR_INTERVAL_SECONDS:-10}s"
        sleep "${RIAK_MONITOR_INTERVAL_SECONDS:-10}"
        if beam_running && ping_works
        then
            log "monitor: BEAM is running and riak ping returned pong"
        else
            log "monitor: OpenRiak stopped responding; container is exiting"
            exit 1
        fi
    done
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
    elif grep -Eq "^[[:space:]]*##[[:space:]]*${escaped_key}[[:space:]]*=" "$config_dir/riak.conf"
    then
        sed -i -E "s|^[[:space:]]*##[[:space:]]*${escaped_key}[[:space:]]*=.*$|${key} = ${value}|" "$config_dir/riak.conf"
    else
        printf '
%s = %s
' "$key" "$value" >> "$config_dir/riak.conf"
    fi
    log "configuration: ${key} = ${value}"
}

node_host=${RIAK_NODE_HOST:-$(hostname)}
riak_node_name=${RIAK_NODE_NAME:-riak@$node_host}
if ! validate_nodename "$riak_node_name"
then
    log "configuration: invalid RIAK_NODE_NAME: ${riak_node_name}"
    exit 1
fi
set_setting nodename "$riak_node_name"
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

wait_for_transfers

cluster_mode=${OPENRIAK_CLUSTER_MODE:-single}
if [ "$cluster_mode" = "single" ]
then
    monitor_node
fi
if [ "$cluster_mode" != "cluster" ]
then
    log "cluster: invalid OPENRIAK_CLUSTER_MODE: ${cluster_mode}"
    exit 1
fi

mkdir -p "$control_dir"
role_value=${role:-follower}
if [ -z "$role_value" ]
then
    role_value=follower
fi

run_follower() {
    log "cluster: Role: Follower"
    clean_owned_control_files
    if cluster_member
    then
        log "cluster: existing multi-node membership detected"
        wait_for_ring
        wait_for_transfers
        monitor_node
    fi

    cluster_waited=0
    cluster_poll=${OPENRIAK_CLUSTER_POLL_SECONDS:-1}
    cluster_timeout=${OPENRIAK_CLUSTER_WAIT_SECONDS:-300}
    while :
    do
        for coordinator_file in "$control_dir/"*-coordinator
        do
            [ -e "$coordinator_file" ] || continue
            coordinator_node=$(sed -n '1p' "$coordinator_file")
            coordinator_suffix=$(sed -n '2p' "$coordinator_file")
            if ! validate_nodename "$coordinator_node"
            then
                log "cluster: ignoring invalid coordinator file $(basename "$coordinator_file")"
                continue
            fi
            if ! printf '%s
' "$coordinator_suffix" | grep -Eq '^[0-9a-f]{16}$'
            then
                log "cluster: ignoring coordinator file with invalid suffix $(basename "$coordinator_file")"
                continue
            fi
            expected_coordinator="$control_dir/${coordinator_node}-${coordinator_suffix}-coordinator"
            if [ "$coordinator_file" != "$expected_coordinator" ]
            then
                log "cluster: ignoring coordinator file whose contents do not match its name"
                continue
            fi
            if cluster_failure_exists "$coordinator_suffix"
            then
                continue
            fi
            ready_file="$control_dir/${riak_node_name}-${coordinator_suffix}-ready"
            approved_file="$control_dir/${riak_node_name}-${coordinator_suffix}-approved"
            joined_file="$control_dir/${riak_node_name}-${coordinator_suffix}-joined"
            complete_file="$control_dir/${riak_node_name}-${coordinator_suffix}-complete"
            if [ ! -e "$ready_file" ] && [ ! -e "$approved_file" ] && [ ! -e "$joined_file" ] && [ ! -e "$complete_file" ]
            then
                atomic_control_file "$ready_file" "$coordinator_node" "$coordinator_suffix"
                log "cluster: announced readiness for coordinator ${coordinator_node} (${coordinator_suffix})"
            fi
        done

        approval_count=0
        selected_approval=
        for approved_candidate in "$control_dir/${riak_node_name}-"*-approved
        do
            [ -e "$approved_candidate" ] || continue
            approval_count=$((approval_count + 1))
            selected_approval=$approved_candidate
        done
        if [ "$approval_count" -gt 1 ]
        then
            log "cluster: conflicting coordinator approvals detected; clearing follower state and retrying"
            clean_owned_control_files
            sleep "$cluster_poll"
            continue
        fi
        if [ "$approval_count" -eq 1 ]
        then
            coordinator_node=$(sed -n '1p' "$selected_approval")
            coordinator_suffix=$(sed -n '2p' "$selected_approval")
            coordinator_file="$control_dir/${coordinator_node}-${coordinator_suffix}-coordinator"
            if [ ! -e "$coordinator_file" ] || ! validate_nodename "$coordinator_node"
            then
                log "cluster: approval no longer has a valid coordinator; clearing follower state"
                clean_owned_control_files
                sleep "$cluster_poll"
                continue
            fi
            log "cluster: join approved by ${coordinator_node} (${coordinator_suffix})"
            if join_output=$(riak_admin_command cluster join "$coordinator_node" 2>&1)
            then
                log_cluster_command_output "join" "$join_output"
                if join_output_is_successful "$join_output"
                then
                    joined_file="$control_dir/${riak_node_name}-${coordinator_suffix}-joined"
                    mv -f "$selected_approval" "$joined_file"
                    log "cluster: join request accepted; waiting for plan and commit"
                    while :
                    do
                        if cluster_failure_exists "$coordinator_suffix"
                        then
                            stop_with_error "another node reported a failure for ${coordinator_suffix}"
                        fi
                        if cluster_member
                        then
                            wait_for_ring
                            wait_for_transfers
                            rm -f "$control_dir/${riak_node_name}-"*
                            log "cluster: follower joined ${coordinator_node} successfully"
                            monitor_node
                        fi
                        sleep "$cluster_poll"
                    done
                fi
            else
                log_cluster_command_output "join" "$join_output"
            fi
            publish_failure "$coordinator_suffix" "cluster join was not accepted for ${coordinator_node}"
        fi

        cluster_waited=$((cluster_waited + cluster_poll))
        if [ "$cluster_waited" -ge "$cluster_timeout" ]
        then
            atomic_control_file "$control_dir/${riak_node_name}-startup-failed" "$riak_node_name" startup
            stop_with_error "no coordinator approved this follower within ${cluster_timeout}s"
        fi
        log "cluster: follower waiting for coordinator approval (${cluster_waited}s/${cluster_timeout}s)"
        sleep "$cluster_poll"
    done
}

run_coordinator() {
    log "cluster: Role: Coordinator"
    for stale_file in "$control_dir/"*-coordinator
    do
        [ -e "$stale_file" ] || continue
        rm -f "$stale_file"
        log "cluster: removed stale coordinator file $(basename "$stale_file")"
    done
    for stale_state in "$control_dir/"*-ready "$control_dir/"*-approved "$control_dir/"*-joined "$control_dir/"*-complete "$control_dir/"*-failed
    do
        [ -e "$stale_state" ] || continue
        rm -f "$stale_state"
        log "cluster: removed stale cluster state $(basename "$stale_state")"
    done
    coordinator_suffix=$(od -An -N8 -tx1 /dev/urandom | tr -d ' \n')
    coordinator_file="$control_dir/${riak_node_name}-${coordinator_suffix}-coordinator"
    atomic_control_file "$coordinator_file" "$riak_node_name" "$coordinator_suffix"
    log "cluster: published coordinator marker $(basename "$coordinator_file")"

    if cluster_member
    then
        log "cluster: existing multi-node membership detected"
        wait_for_ring
        wait_for_transfers
    fi

    cluster_poll=${OPENRIAK_CLUSTER_POLL_SECONDS:-1}
    while :
    do
        for failure_file in "$control_dir/"*-failed
        do
            [ -e "$failure_file" ] || continue
            atomic_control_file "$control_dir/${riak_node_name}-${coordinator_suffix}-failed" "$riak_node_name" "$coordinator_suffix"
            stop_with_error "cluster participant reported failure in $(basename "$failure_file")"
        done

        for ready_file in "$control_dir/"*-"${coordinator_suffix}"-ready
        do
            [ -e "$ready_file" ] || continue
            requested_coordinator=$(sed -n '1p' "$ready_file")
            requested_suffix=$(sed -n '2p' "$ready_file")
            if [ "$requested_coordinator" != "$riak_node_name" ] || [ "$requested_suffix" != "$coordinator_suffix" ]
            then
                log "cluster: rejecting malformed readiness file $(basename "$ready_file")"
                rm -f "$ready_file"
                continue
            fi
            approved_file=${ready_file%-ready}-approved
            mv -f "$ready_file" "$approved_file"
            log "cluster: approved follower $(basename "${approved_file%-approved}")"
        done

        joined_count=0
        for joined_file in "$control_dir/"*-"${coordinator_suffix}"-joined
        do
            [ -e "$joined_file" ] || continue
            joined_count=$((joined_count + 1))
        done
        if [ "$joined_count" -gt 0 ]
        then
            log "cluster: planning a batch of ${joined_count} joined node(s)"
            if plan_output=$(riak_admin_command cluster plan 2>&1)
            then
                log_cluster_command_output "plan" "$plan_output"
                if ! plan_output_is_successful "$plan_output"
                then
                    publish_failure "$coordinator_suffix" "cluster plan was not accepted"
                fi
            else
                log_cluster_command_output "plan" "$plan_output"
                publish_failure "$coordinator_suffix" "cluster plan command failed"
            fi
            log "cluster: committing the planned membership changes"
            if commit_output=$(riak_admin_command cluster commit 2>&1)
            then
                log_cluster_command_output "commit" "$commit_output"
                if ! commit_output_is_successful "$commit_output"
                then
                    publish_failure "$coordinator_suffix" "cluster commit was not accepted"
                fi
            else
                log_cluster_command_output "commit" "$commit_output"
                publish_failure "$coordinator_suffix" "cluster commit command failed"
            fi
            wait_for_ring
            wait_for_transfers
            for joined_file in "$control_dir/"*-"${coordinator_suffix}"-joined
            do
                [ -e "$joined_file" ] || continue
                complete_file=${joined_file%-joined}-complete
                mv -f "$joined_file" "$complete_file"
                log "cluster: completed follower $(basename "${complete_file%-complete}")"
            done
        fi

        if beam_running && ping_works
        then
            log "monitor: Coordinator is healthy; sleeping for ${cluster_poll}s"
        else
            atomic_control_file "$control_dir/${riak_node_name}-${coordinator_suffix}-failed" "$riak_node_name" "$coordinator_suffix"
            stop_with_error "coordinator health check failed"
        fi
        sleep "$cluster_poll"
    done
}

case "$role_value" in
    coordinator)
        run_coordinator
        ;;
    follower)
        run_follower
        ;;
    *)
        log "cluster: invalid role value: ${role_value}"
        exit 1
        ;;
esac
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
