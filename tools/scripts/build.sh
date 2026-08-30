#!/usr/bin/env sh
set -eu

site_root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
required_version=$(tr -d '\r\n' < "$site_root/.hugo-version")

case "$(hugo version)" in
  *"hugo v${required_version}"*) ;;
  *) echo "This site requires Hugo ${required_version}." >&2; exit 1 ;;
esac

base_url=${HUGO_BASEURL:-https://www.openriak.org/docs/}
case "$base_url" in */) ;; *) base_url="${base_url}/" ;; esac
destination=${HUGO_DESTINATION:-$site_root/public}
# These names are also Hugo configuration environment variables. Capture the
# wrapper inputs, then unset them so each project's explicit flags take effect.
unset HUGO_BASEURL HUGO_DESTINATION

if command -v node >/dev/null 2>&1; then
  node "$site_root/tools/scripts/sync-product-metadata.js"
fi

set -- --source "$site_root/content" --destination "$destination" --baseURL "$base_url" --gc --minify --panicOnWarning --noBuildLock --cleanDestinationDir
if [ "${INCLUDE_DRAFTS:-true}" = "true" ]; then set -- "$@" --buildDrafts; fi
hugo "$@"
