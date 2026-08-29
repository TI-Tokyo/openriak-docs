#!/usr/bin/env sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
site_root=$(CDPATH= cd -- "$script_dir/.." && pwd)
compose_file="$script_dir/docker-compose.localhost-preview.yaml"
preview_url=${HUGO_BASEURL:-http://localhost:1314/docs/}

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is required but was not found on PATH." >&2
  exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "Docker Compose v2 is required (the 'docker compose' command)." >&2
  exit 1
fi

echo "Starting OpenRiak docs with Hugo 0.165.0"
echo "HTTP preview: $preview_url"
exec docker compose --project-directory "$site_root" -f "$compose_file" up --remove-orphans "$@"
