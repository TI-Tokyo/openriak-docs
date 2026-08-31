#!/usr/bin/env sh
set -eu

docker_directory=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
compose_file="$docker_directory/compose.yaml"
native_docker_found=false
mkdir -p "$docker_directory/../build/archives"

build_profile=development
case "${1:-}" in
  development|beta-test|release) build_profile=$1; shift ;;
esac
export OPENRIAK_DOCS_BUILD_PROFILE=$build_profile

if [ "$build_profile" = release ]; then
  compose_profile=release
else
  compose_profile=
fi

find_zoneinfo_directory() {
  timezone=$1
  for candidate in \
    "${OPENRIAK_DOCS_ZONEINFO_DIR:-}" \
    /usr/share/zoneinfo \
    /var/db/timezone/zoneinfo
  do
    if [ -n "$candidate" ] && [ -e "$candidate/$timezone" ]; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done
  return 1
}

detect_host_timezone() {
  if [ -n "${OPENRIAK_DOCS_TZ:-}" ]; then
    printf '%s\n' "$OPENRIAK_DOCS_TZ"
    return 0
  fi

  if [ -r /etc/timezone ]; then
    timezone=$(tr -d '[:space:]' < /etc/timezone)
    if [ -n "$timezone" ]; then
      printf '%s\n' "$timezone"
      return 0
    fi
  fi

  localtime_target=$(readlink /etc/localtime 2>/dev/null || true)
  case "$localtime_target" in
    */zoneinfo/*)
      printf '%s\n' "${localtime_target#*/zoneinfo/}"
      return 0
      ;;
  esac

  if [ -n "${TZ:-}" ] && [ "${TZ#/}" = "$TZ" ] && [ "${TZ#:}" = "$TZ" ]; then
    printf '%s\n' "$TZ"
    return 0
  fi
  return 1
}

host_timezone=$(detect_host_timezone || true)
zoneinfo_directory=$(find_zoneinfo_directory "$host_timezone" || true)
if [ -z "$zoneinfo_directory" ] || [ -z "$host_timezone" ]; then
  echo 'Unable to detect a usable IANA host timezone.' >&2
  echo 'Set OPENRIAK_DOCS_TZ and OPENRIAK_DOCS_ZONEINFO_DIR, then rerun this command.' >&2
  exit 1
fi

export OPENRIAK_DOCS_TZ="$host_timezone"
export OPENRIAK_DOCS_ZONEINFO_DIR="$zoneinfo_directory"

if command -v docker >/dev/null 2>&1; then
  native_docker_found=true
  if docker info >/dev/null 2>&1; then
    if docker compose version >/dev/null 2>&1; then
      if [ -n "$compose_profile" ]; then
        exec docker compose --file "$compose_file" --profile "$compose_profile" up "$@"
      fi
      docker compose --file "$compose_file" --profile release stop archives >/dev/null 2>&1 || true
      exec docker compose --file "$compose_file" up "$@"
    fi

    if command -v docker-compose >/dev/null 2>&1; then
      if [ -n "$compose_profile" ]; then
        exec docker-compose --file "$compose_file" --profile "$compose_profile" up "$@"
      fi
      docker-compose --file "$compose_file" --profile release stop archives >/dev/null 2>&1 || true
      exec docker-compose --file "$compose_file" up "$@"
    fi

    echo 'Docker is running, but Docker Compose is unavailable.' >&2
    echo 'Install the Docker Compose plugin, then rerun ./docker/run.local.sh.' >&2
    exit 1
  fi
fi

if command -v docker.exe >/dev/null 2>&1 && command -v wslpath >/dev/null 2>&1; then
  if docker.exe info >/dev/null 2>&1 && docker.exe compose version >/dev/null 2>&1; then
    export OPENRIAK_DOCS_ZONEINFO_DIR=$(wslpath -w "$zoneinfo_directory")
    export WSLENV="${WSLENV:+$WSLENV:}OPENRIAK_DOCS_TZ:OPENRIAK_DOCS_ZONEINFO_DIR"
    if [ -n "$compose_profile" ]; then
      exec docker.exe compose --file "$(wslpath -w "$compose_file")" --profile "$compose_profile" up "$@"
    fi
    docker.exe compose --file "$(wslpath -w "$compose_file")" --profile release stop archives >/dev/null 2>&1 || true
    exec docker.exe compose --file "$(wslpath -w "$compose_file")" up "$@"
  fi
fi

echo 'Unable to start the site because the Docker daemon is not accessible.' >&2
echo >&2

if [ "$native_docker_found" = true ]; then
  if [ "$(id -u)" -ne 0 ]; then
    echo 'If Docker requires elevated socket access, try:' >&2
    echo '  sudo ./docker/run.local.sh' >&2
    echo >&2
    echo 'For a lasting Linux setup, add your user to the docker group and then sign out and back in:' >&2
    echo '  sudo usermod -aG docker "$USER"' >&2
    echo >&2
  else
    echo 'Docker is still unavailable as root; make sure the Docker daemon is running.' >&2
    echo >&2
  fi
else
  echo 'Install Docker Desktop or Docker Engine with the Docker Compose plugin.' >&2
  echo >&2
fi

if command -v wslpath >/dev/null 2>&1; then
  echo 'On WSL, start Docker Desktop and enable WSL integration for this distribution.' >&2
else
  echo 'Start Docker Desktop, or on systemd Linux run: sudo systemctl start docker' >&2
fi

exit 1
