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
mkdir -p /opt/openriak-defaults/etc-riak /var/lib/riak /var/log/riak /run/riak
cp -a /etc/riak/. /opt/openriak-defaults/etc-riak/
chown -R riak:riak /var/lib/riak /var/log/riak /run/riak
OPENRIAK_IMAGE_SETUP

COPY <<'OPENRIAK_ENTRYPOINT' /usr/local/bin/openriak-entrypoint
#!/bin/sh
set -eu

config_dir=/etc/riak
data_dir=/var/lib/riak
log_dir=/var/log/riak
defaults_dir=/opt/openriak-defaults/etc-riak

mkdir -p "$config_dir" "$data_dir" "$log_dir" /run/riak
if [ ! -s "$config_dir/riak.conf" ]
then
    cp -a "$defaults_dir/." "$config_dir/"
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
    exit 0
fi

ulimit -n "${RIAK_NOFILE_LIMIT:-100000}"
if command -v su-exec >/dev/null 2>&1
then
    exec su-exec riak /usr/sbin/riak console
fi
if command -v runuser >/dev/null 2>&1
then
    exec runuser -u riak -- /usr/sbin/riak console
fi
exec su -s /bin/sh riak -c 'exec /usr/sbin/riak console'
OPENRIAK_ENTRYPOINT

RUN chmod 0755 /usr/local/bin/openriak-entrypoint

VOLUME ["/etc/riak"]
VOLUME ["/var/lib/riak"]
VOLUME ["/var/log/riak"]
EXPOSE 8087
EXPOSE 8098
ENTRYPOINT ["/usr/local/bin/openriak-entrypoint"]
