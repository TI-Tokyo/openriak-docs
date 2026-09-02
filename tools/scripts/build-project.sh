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
build_profile=${OPENRIAK_DOCS_BUILD_PROFILE:-release}
development_riak_kv_version=${OPENRIAK_DOCS_RIAK_KV_VERSION:-3.2.5}
if [ -z "$destination" ]; then
  echo 'Usage: build-project.sh core|archives DESTINATION' >&2
  exit 2
fi

case "$build_profile" in development|beta-test|release) ;; *)
  echo 'OPENRIAK_DOCS_BUILD_PROFILE must be development, beta-test, or release.' >&2
  exit 2
esac

base_url=${HUGO_BASEURL:-https://www.openriak.org/docs/}
case "$base_url" in */) ;; *) base_url="${base_url}/" ;; esac
unset HUGO_BASEURL HUGO_DESTINATION

case "$project" in
  core)
    if [ "$build_profile" = development ]; then
      generated_config=${HUGO_GENERATED_CONFIG:-$site_root/build/generated-development/hugo.yaml}
      development_data_root=${OPENRIAK_DOCS_DEVELOPMENT_DATA_ROOT:-$site_root/build/generated-development}
    else
      generated_config=${HUGO_GENERATED_CONFIG:-$site_root/tools/generated/hugo.yaml}
    fi
    if ! command -v node >/dev/null 2>&1; then
      echo 'Node.js is required to generate product version mounts.' >&2
      exit 1
    fi
    if [ "$build_profile" = development ]; then
      node "$site_root/tools/scripts/generate-version-mounts.js" \
        --base-config "$site_root/content/hugo.yaml" \
        --output "$generated_config" \
        --version-data-root "openriak-kv=$development_data_root/openriak-kv/data/versions" \
        --version-data-root "openriak-cs=$development_data_root/openriak-cs/data/versions" \
        --version-data-root "openriak-ts=$development_data_root/openriak-ts/data/versions" \
        --include-version "riak-kv=$development_riak_kv_version" \
        --include-latest riak-cs \
        --include-latest riak-ts
      node "$site_root/tools/scripts/sync-product-metadata.js" \
        --output-root "$development_data_root" \
        --include-version "riak-kv=$development_riak_kv_version" \
        --include-latest riak-cs \
        --include-latest riak-ts
    else
      node "$site_root/tools/scripts/generate-version-mounts.js" \
        --base-config "$site_root/content/hugo.yaml" \
        --output "$generated_config"
      node "$site_root/tools/scripts/sync-product-metadata.js"
    fi
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
