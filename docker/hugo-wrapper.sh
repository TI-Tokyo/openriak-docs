#!/bin/sh
exec /opt/hugo/lib/ld-musl-*.so.1 --library-path /opt/hugo/lib /opt/hugo/hugo "$@"
