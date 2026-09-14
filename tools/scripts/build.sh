#!/usr/bin/env sh
set -eu

for argument in "$@"; do
  case "$argument" in -h|--help)
    cat <<'OPENRIAK_HELP'
Build the OpenRiak documentation site and replace the assembled destination.
Release builds include archives; development and beta-test build the core site.

Usage: build.sh [development|beta-test|release]

Arguments:
  PROFILE                       Build profile (default: release).
                                development limits historical product versions;
                                beta-test builds all core versions without archives.
  -h, --help                    Show help and exit without building or changing files.

Environment:
  HUGO_DESTINATION              Assembled destination (default: repository public/).
  HUGO_CORE_DESTINATION         Core build (default: build/core-PROFILE/).
  HUGO_ARCHIVE_DESTINATION      Archive build (default: build/archives/).
  HUGO_BASEURL                  Published URL (default: https://www.openriak.org/docs/).
  INCLUDE_DRAFTS                Include draft pages when true (default: true).
  OPENRIAK_DOCS_RIAK_KV_VERSION Development Riak KV version (default: 3.2.5).
  HUGO_GENERATED_CONFIG         Override generated core config path.
  OPENRIAK_DOCS_DEVELOPMENT_DATA_ROOT
                                Development metadata root (default: build/generated-development/).

Requires Node.js and the Hugo version in .hugo-version.
Default paths are relative to the repository; explicit paths use the current directory.
OPENRIAK_HELP
    exit 0
    ;;
  esac
done

site_root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
build_profile=${1:-release}
destination=${HUGO_DESTINATION:-$site_root/public}
core_destination=${HUGO_CORE_DESTINATION:-$site_root/build/core-$build_profile}
archive_destination=${HUGO_ARCHIVE_DESTINATION:-$site_root/build/archives}

case "$build_profile" in development|beta-test|release) ;; *)
  echo 'Usage: build.sh [development|beta-test|release]' >&2
  exit 2
esac

export OPENRIAK_DOCS_BUILD_PROFILE=$build_profile

"$site_root/tools/scripts/build-project.sh" core "$core_destination"
if [ "$build_profile" = release ]; then
  "$site_root/tools/scripts/build-project.sh" archives "$archive_destination"
  "$site_root/tools/scripts/assemble-site.sh" "$core_destination" "$archive_destination" "$destination"
else
  rm -rf "$destination"
  mv "$core_destination" "$destination"
fi

printf 'Built the %s static site in %s\n' "$build_profile" "$destination"
