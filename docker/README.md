# Docker

Docker provides split local development and one assembled production artifact.

## Local development profiles

From the repository root:

```sh
./docker/run.local.sh development
```

This starts `core` and `gateway`. The core mount generator includes all active
OpenRiak documentation but only Riak KV `3.2.5`, substantially reducing the
historical page set watched and rendered by Hugo. Choose another historical
release when needed:

```sh
OPENRIAK_DOCS_RIAK_KV_VERSION=2.0.0 ./docker/run.local.sh development
```

The other profiles are:

```sh
./docker/run.local.sh beta-test  # all core versions; no archive Hugo process
./docker/run.local.sh release    # all core versions plus the archive process
```

The services are:

- `core` — homepage, Community, products, shared assets, and live reload.
- `archives` — Archived Technical Blog and Archived Mailing List; started only by the `release` profile.
- `gateway` — presents both Hugo servers at `127.0.0.1:1410`.

The services use separate Hugo caches. Arguments are forwarded to
`docker compose up`; `./docker/run.local.sh -d` starts them in the background.
The wrapper detects and passes through the host IANA timezone.
Switching from `release` to either core-only profile stops the archive service.

The archive server writes its completed render to `build/archives/`. Development
and beta-test previews continue serving that cached output when present. After a
release preview has built it, the archive service can be stopped with:

```sh
docker compose -f docker/compose.yaml stop archives
```

The gateway then serves that last successful archive output directly while the
core Hugo server continues rebuilding. Start `archives` again after changing an
archive or shared template.

## Static rsync artifact

```sh
./docker/build.static.sh release
```

The multi-stage image builds core and archives independently and rejects
overlapping output paths. The export container copies the selected artifact
through the bind-mounted `docker-wip/` staging directory; after the container
exits, the host script moves that tree to `public/`. Rsync `public/` to the
server directory corresponding to the path in `HUGO_BASEURL`.

`./docker/build.static.sh development` exports core with one selected Riak KV
release. `./docker/build.static.sh beta-test` exports core with all releases.
Those artifacts deliberately omit the archives and are not deployment builds.

Docker reuses the archive stage when only active documentation changes. Changes to
shared templates invalidate both affected stages, as required.

## Nginx runtime image

```sh
docker build -f docker/Dockerfile --build-arg HUGO_BASEURL=https://www.openriak.org/docs/ -t openriak-docs .
```

This final image contains the assembled site under the base URL path. Public
servers need only the exported static files; the runtime image is optional.
