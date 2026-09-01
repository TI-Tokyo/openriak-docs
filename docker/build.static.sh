#!/usr/bin/env sh
set -eu

repository_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
build_profile=${1:-release}
staging="$repository_root/docker-wip"
destination="$repository_root/public"
base_url=${HUGO_BASEURL:-https://www.openriak.org/docs/}
include_drafts=${INCLUDE_DRAFTS:-true}
riak_kv_version=${OPENRIAK_DOCS_RIAK_KV_VERSION:-3.2.5}
export_image="openriak-docs-static-export:${build_profile}-$$"
docker_cli=

case "$build_profile" in
  development|beta-test) docker_target=core-build ;;
  release) docker_target=assembled ;;
  *) echo 'Usage: build.static.sh [development|beta-test|release]' >&2; exit 2 ;;
esac

cleanup_image() {
  if [ -n "$docker_cli" ]; then "$docker_cli" image rm "$export_image" >/dev/null 2>&1 || true; fi
}
trap cleanup_image 0

rm -rf "$staging"
mkdir -p "$staging"

if command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
  docker_cli=docker
  docker build --file "$repository_root/docker/Dockerfile" --target "$docker_target" \
    --build-arg "CORE_BUILD_PROFILE=$build_profile" --build-arg "RIAK_KV_VERSION=$riak_kv_version" \
    --build-arg "HUGO_BASEURL=$base_url" --build-arg "INCLUDE_DRAFTS=$include_drafts" \
    --tag "$export_image" "$repository_root"
  docker run --rm --user "$(id -u):$(id -g)" --entrypoint sh \
    --mount "type=bind,source=$staging,target=/output" \
    "$export_image" -c 'cp -a /project/public/. /output/'
elif command -v docker.exe >/dev/null 2>&1 && command -v wslpath >/dev/null 2>&1 && docker.exe info >/dev/null 2>&1; then
  docker_cli=docker.exe
  repository_windows=$(wslpath -w "$repository_root")
  staging_windows=$(wslpath -w "$staging")
  docker.exe build --file "$repository_windows\\docker\\Dockerfile" --target "$docker_target" \
    --build-arg "CORE_BUILD_PROFILE=$build_profile" --build-arg "RIAK_KV_VERSION=$riak_kv_version" \
    --build-arg "HUGO_BASEURL=$base_url" --build-arg "INCLUDE_DRAFTS=$include_drafts" \
    --tag "$export_image" "$repository_windows"
  docker.exe run --rm --user "$(id -u):$(id -g)" --entrypoint sh \
    --mount "type=bind,source=$staging_windows,target=/output" \
    "$export_image" -c 'cp -a /project/public/. /output/'
else
  echo 'Unable to build because the Docker daemon is not accessible.' >&2
  exit 1
fi

rm -rf "$destination"
mv "$staging" "$destination"
printf 'Exported the %s static site to %s\n' "$build_profile" "$destination"
