#!/usr/bin/env sh
set -eu

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
