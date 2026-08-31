#!/usr/bin/env sh
set -eu

repository_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
staging="$repository_root/build/docker-static"
destination="$repository_root/public"
base_url=${HUGO_BASEURL:-https://www.openriak.org/docs/}
include_drafts=${INCLUDE_DRAFTS:-true}

rm -rf "$staging"
mkdir -p "$staging"

if command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
  docker build --file "$repository_root/docker/Dockerfile" --target static \
    --build-arg "HUGO_BASEURL=$base_url" --build-arg "INCLUDE_DRAFTS=$include_drafts" \
    --output "type=local,dest=$staging" "$repository_root"
elif command -v docker.exe >/dev/null 2>&1 && command -v wslpath >/dev/null 2>&1 && docker.exe info >/dev/null 2>&1; then
  repository_windows=$(wslpath -w "$repository_root")
  staging_windows=$(wslpath -w "$staging")
  docker.exe build --file "$repository_windows\\docker\\Dockerfile" --target static \
    --build-arg "HUGO_BASEURL=$base_url" --build-arg "INCLUDE_DRAFTS=$include_drafts" \
    --output "type=local,dest=$staging_windows" "$repository_windows"
else
  echo 'Unable to build because the Docker daemon is not accessible.' >&2
  exit 1
fi

rm -rf "$destination"
mv "$staging" "$destination"
printf 'Exported the complete static site to %s\n' "$destination"
