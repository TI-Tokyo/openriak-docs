# syntax=docker/dockerfile:1.7
# Generated and tested by tools/openriak-docker/openriak-docker. Do not edit by hand.
FROM --platform=linux/amd64 alpine:3.21@sha256:48b0309ca019d89d40f670aa1bc06e426dc0931948452e8491e3d65087abc07d

ADD --checksum=sha256:140f1decb585e5855990c140b58afcb2ba3629e5dc65fffab8d0eaaa0621cc69 https://files.tiot.jp/alpine/v3.21/main/x86_64/riak-3.4.0.24-r1.apk /tmp/riak-3.4.0.24-r1.apk
RUN apk add --no-cache bash ca-certificates curl su-exec && apk add --no-cache --allow-untrusted /tmp/riak-3.4.0.24-r1.apk && rm -f /tmp/riak-3.4.0.24-r1.apk
RUN getent group riak >/dev/null 2>&1 || addgroup -S riak; id riak >/dev/null 2>&1 || adduser -S -D -H -h /var/lib/riak -s /sbin/nologin -G riak riak && \
    test -x /usr/sbin/riak && id riak && \
    mkdir -p /opt/openriak-defaults/etc-riak /var/lib/riak /var/log/riak /run/riak && \
    cp -a /etc/riak/. /opt/openriak-defaults/etc-riak/ && \
    printf '%s' 'IyEvYmluL3NoCnNldCAtZXUKCmNvbmZpZ19kaXI9L2V0Yy9yaWFrCmRhdGFfZGlyPS92YXIvbGliL3JpYWsKbG9nX2Rpcj0vdmFyL2xvZy9yaWFrCmRlZmF1bHRzX2Rpcj0vb3B0L29wZW5yaWFrLWRlZmF1bHRzL2V0Yy1yaWFrCgpta2RpciAtcCAiJGNvbmZpZ19kaXIiICIkZGF0YV9kaXIiICIkbG9nX2RpciIgL3J1bi9yaWFrCmlmIFsgISAtcyAiJGNvbmZpZ19kaXIvcmlhay5jb25mIiBdOyB0aGVuCiAgICBjcCAtYSAiJGRlZmF1bHRzX2Rpci8uIiAiJGNvbmZpZ19kaXIvIgpmaQoKc2V0X3NldHRpbmcoKSB7CiAgICBrZXk9JDEKICAgIHZhbHVlPSQyCiAgICBlc2NhcGVkX2tleT0kKHByaW50ZiAnJXMnICIka2V5IiB8IHNlZCAncy9bLltcKl4kKCkrP3t8XS9cXCYvZycpCiAgICBpZiBncmVwIC1FcSAiXltbOnNwYWNlOl1dKiR7ZXNjYXBlZF9rZXl9W1s6c3BhY2U6XV0qPSIgIiRjb25maWdfZGlyL3JpYWsuY29uZiI7IHRoZW4KICAgICAgICBzZWQgLWkgLUUgInN8XltbOnNwYWNlOl1dKiR7ZXNjYXBlZF9rZXl9W1s6c3BhY2U6XV0qPS4qJHwke2tleX0gPSAke3ZhbHVlfXwiICIkY29uZmlnX2Rpci9yaWFrLmNvbmYiCiAgICBlbHNlCiAgICAgICAgcHJpbnRmICcKJXMgPSAlcwonICIka2V5IiAiJHZhbHVlIiA+PiAiJGNvbmZpZ19kaXIvcmlhay5jb25mIgogICAgZmkKfQoKbm9kZV9ob3N0PSR7UklBS19OT0RFX0hPU1Q6LSQoaG9zdG5hbWUpfQpzZXRfc2V0dGluZyBub2RlbmFtZSAiJHtSSUFLX05PREVfTkFNRTotcmlha0Akbm9kZV9ob3N0fSIKc2V0X3NldHRpbmcgbGlzdGVuZXIuaHR0cC5pbnRlcm5hbCAiMC4wLjAuMDo4MDk4IgpzZXRfc2V0dGluZyBsaXN0ZW5lci5wcm90b2J1Zi5pbnRlcm5hbCAiMC4wLjAuMDo4MDg3IgoKY2hvd24gLVIgcmlhazpyaWFrICIkY29uZmlnX2RpciIgIiRkYXRhX2RpciIgIiRsb2dfZGlyIiAvcnVuL3JpYWsKaWYgWyAiJHtSSUFLX0lOSVRfT05MWTotMH0iID0gIjEiIF07IHRoZW4KICAgIGV4aXQgMApmaQoKdWxpbWl0IC1uICIke1JJQUtfTk9GSUxFX0xJTUlUOi0xMDAwMDB9IgppZiBjb21tYW5kIC12IHN1LWV4ZWMgPi9kZXYvbnVsbCAyPiYxOyB0aGVuCiAgICBleGVjIHN1LWV4ZWMgcmlhayAvdXNyL3NiaW4vcmlhayBjb25zb2xlCmZpCmlmIGNvbW1hbmQgLXYgcnVudXNlciA+L2Rldi9udWxsIDI+JjE7IHRoZW4KICAgIGV4ZWMgcnVudXNlciAtdSByaWFrIC0tIC91c3Ivc2Jpbi9yaWFrIGNvbnNvbGUKZmkKZXhlYyBzdSAtcyAvYmluL3NoIHJpYWsgLWMgJ2V4ZWMgL3Vzci9zYmluL3JpYWsgY29uc29sZScK' | base64 -d > /usr/local/bin/openriak-entrypoint && \
    chmod 0755 /usr/local/bin/openriak-entrypoint && \
    chown -R riak:riak /var/lib/riak /var/log/riak /run/riak

ENV RIAK_NOFILE_LIMIT=100000
VOLUME ["/etc/riak", "/var/lib/riak", "/var/log/riak"]
EXPOSE 8087 8098
ENTRYPOINT ["/usr/local/bin/openriak-entrypoint"]
