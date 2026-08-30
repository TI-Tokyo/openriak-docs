# Docker

Container build and local single-process Hugo preview configuration.

From the repository root, start the complete site with one Hugo server:

```sh
./docker/run.local.sh
```

Arguments are forwarded to `docker compose up`; for example,
`./docker/run.local.sh -d` starts the services in the background.

The wrapper supports native Docker, the legacy `docker-compose` command, and
Docker Desktop from WSL. If Docker cannot be reached, it prints platform-aware
recovery suggestions, including when retrying with `sudo` may be appropriate.

Build the production Nginx image with:

```sh
docker build -f docker/Dockerfile --build-arg HUGO_BASEURL=https://www.openriak.org/docs/ -t openriak-docs .
```

The Compose service binds only to `127.0.0.1` on port 1410.
