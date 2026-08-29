#!/usr/bin/env sh
set -eu

site_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
required_version=$(tr -d '\r\n' < "$site_root/.hugo-version")

case "$(hugo version)" in
  *"hugo v${required_version}"*) ;;
  *) echo "This site requires Hugo ${required_version}." >&2; exit 1 ;;
esac

set -- --source "$site_root" --destination "$site_root/public" --gc --minify --panicOnWarning
if [ "${INCLUDE_DRAFTS:-true}" = "true" ]; then
  set -- "$@" --buildDrafts
fi
if [ -n "${HUGO_BASEURL:-}" ]; then
  set -- "$@" --baseURL "$HUGO_BASEURL"
fi

exec hugo "$@"
