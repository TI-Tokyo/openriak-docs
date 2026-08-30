#!/usr/bin/env sh
set -eu

docker_directory=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
compose_file="$docker_directory/compose.yaml"
native_docker_found=false

if command -v docker >/dev/null 2>&1; then
  native_docker_found=true
  if docker info >/dev/null 2>&1; then
    if docker compose version >/dev/null 2>&1; then
      exec docker compose --file "$compose_file" up "$@"
    fi

    if command -v docker-compose >/dev/null 2>&1; then
      exec docker-compose --file "$compose_file" up "$@"
    fi

    echo 'Docker is running, but Docker Compose is unavailable.' >&2
    echo 'Install the Docker Compose plugin, then rerun ./docker/run.local.sh.' >&2
    exit 1
  fi
fi

if command -v docker.exe >/dev/null 2>&1 && command -v wslpath >/dev/null 2>&1; then
  if docker.exe info >/dev/null 2>&1 && docker.exe compose version >/dev/null 2>&1; then
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
