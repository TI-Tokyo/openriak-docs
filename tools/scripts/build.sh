#!/usr/bin/env sh
set -eu

site_root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
destination=${HUGO_DESTINATION:-$site_root/public}
core_destination=${HUGO_CORE_DESTINATION:-$site_root/build/core}
archive_destination=${HUGO_ARCHIVE_DESTINATION:-$site_root/build/archives}

"$site_root/tools/scripts/build-project.sh" core "$core_destination"
"$site_root/tools/scripts/build-project.sh" archives "$archive_destination"
"$site_root/tools/scripts/assemble-site.sh" "$core_destination" "$archive_destination" "$destination"

printf 'Assembled the complete static site in %s\n' "$destination"
