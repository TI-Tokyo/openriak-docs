#!/usr/bin/env sh
set -eu

site_root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
required_version=$(tr -d '\r\n' < "$site_root/.hugo-version")

case "$(hugo version)" in
  *"hugo v${required_version}"*) ;;
  *) echo "This site requires Hugo ${required_version}." >&2; exit 1 ;;
esac

project=${1:-}
destination=${2:-}
if [ -z "$destination" ]; then
  echo 'Usage: build-project.sh core|archives DESTINATION' >&2
  exit 2
fi

base_url=${HUGO_BASEURL:-https://www.openriak.org/docs/}
case "$base_url" in */) ;; *) base_url="${base_url}/" ;; esac
unset HUGO_BASEURL HUGO_DESTINATION

case "$project" in
  core)
    generated_config=${HUGO_GENERATED_CONFIG:-$site_root/tools/generated/hugo.yaml}
    if ! command -v node >/dev/null 2>&1; then
      echo 'Node.js is required to generate product version mounts.' >&2
      exit 1
    fi
    node "$site_root/tools/scripts/generate-version-mounts.js" \
      --base-config "$site_root/content/hugo.yaml" \
      --output "$generated_config"
    node "$site_root/tools/scripts/sync-product-metadata.js"
    config=$generated_config
    ;;
  archives)
    config=$site_root/content/hugo-archives.yaml
    ;;
  *)
    echo 'Usage: build-project.sh core|archives DESTINATION' >&2
    exit 2
    ;;
esac

set -- --source "$site_root/content" --config "$config" --destination "$destination" \
  --baseURL "$base_url" --gc --minify --panicOnWarning --noBuildLock --cleanDestinationDir
if [ "${INCLUDE_DRAFTS:-true}" = "true" ]; then set -- "$@" --buildDrafts; fi
hugo "$@"
