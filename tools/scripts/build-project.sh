#!/usr/bin/env sh
set -eu

for argument in "$@"; do
  case "$argument" in -h|--help)
    cat <<'OPENRIAK_HELP'
Build one Hugo project, regenerating core metadata when building core.
The destination is cleaned as part of the Hugo build.

Usage: build-project.sh core|archives DESTINATION

Arguments:
  core|archives                 Project to build (required).
  DESTINATION                   Build output directory (required).
  -h, --help                    Show help and exit without checking tools or building.

Environment:
  OPENRIAK_DOCS_BUILD_PROFILE   development, beta-test or release (default: release).
  OPENRIAK_DOCS_RIAK_KV_VERSION Development Riak KV version (default: 3.2.5).
  HUGO_BASEURL                  Published URL (default: https://www.openriak.org/docs/).
  INCLUDE_DRAFTS                Include draft pages when true (default: true).
  HUGO_GENERATED_CONFIG         Generated core config (default: tools/generated/hugo.yaml;
                                development: build/generated-development/hugo.yaml).
  OPENRIAK_DOCS_DEVELOPMENT_DATA_ROOT
                                Development metadata root (default: build/generated-development/).

Requires the Hugo version in .hugo-version; core also requires Node.js.
Default paths are relative to the repository.
OPENRIAK_HELP
    exit 0
    ;;
  esac
done

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
    elif [ -n "${OPENRIAK_DOCS_DEVELOPMENT_DATA_ROOT:-}" ]; then
      # Isolated semantic exports can render every version without rewriting
      # the repository's generated metadata.
      node "$site_root/tools/scripts/generate-version-mounts.js" \
        --base-config "$site_root/content/hugo.yaml" --output "$generated_config" \
        --version-data-root "openriak-kv=$OPENRIAK_DOCS_DEVELOPMENT_DATA_ROOT/openriak-kv/data/versions" \
        --version-data-root "openriak-cs=$OPENRIAK_DOCS_DEVELOPMENT_DATA_ROOT/openriak-cs/data/versions" \
        --version-data-root "openriak-ts=$OPENRIAK_DOCS_DEVELOPMENT_DATA_ROOT/openriak-ts/data/versions"
      node "$site_root/tools/scripts/sync-product-metadata.js" --output-root "$OPENRIAK_DOCS_DEVELOPMENT_DATA_ROOT"
    else
      node "$site_root/tools/scripts/generate-version-mounts.js" \
        --base-config "$site_root/content/hugo.yaml" \
        --output "$generated_config"
      node "$site_root/tools/scripts/sync-product-metadata.js"
    fi
    node "$site_root/tools/scripts/render-mermaid.mjs"
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
  --baseURL "$base_url" --gc --minify --noBuildLock --cleanDestinationDir
# Invalid optional social images warn and fall back in both projects.
if [ "${INCLUDE_DRAFTS:-true}" = "true" ]; then set -- "$@" --buildDrafts; fi
if [ "${OPENRIAK_SEMANTIC_EXPORT_ONLY:-0}" = 1 ]; then set -- "$@" --renderSegments semantic; fi
hugo "$@"
if [ "$project" = core ] && [ "${OPENRIAK_SEMANTIC_EXPORT_ONLY:-0}" != 1 ]; then
  node "$site_root/tools/scripts/check-social-metadata.cjs" "$destination" "$base_url"
  node "$site_root/tools/scripts/build-semantic-index.mjs" --ensure --all --site-dir "$destination" --publish-dir "$destination"
fi
