# Docker

Docker provides split local development and one assembled production artifact.

## Local development

From the repository root:

```sh
./docker/run.local.sh
```

Compose starts:

- `core` — homepage, Community, products, shared assets, and live reload.
- `archives` — Archived Technical Blog and Archived Mailing List.
- `gateway` — presents both Hugo servers at `127.0.0.1:1410`.

The services use separate Hugo caches. Arguments are forwarded to
`docker compose up`; `./docker/run.local.sh -d` starts them in the background.
The wrapper detects and passes through the host IANA timezone.

The archive server writes its completed render to `build/archives/`. After the
first successful archive build, it can be stopped with:

```sh
docker compose -f docker/compose.yaml stop archives
```

The gateway then serves that last successful archive output directly while the
core Hugo server continues rebuilding. Start `archives` again after changing an
archive or shared template.

## Static rsync artifact

```sh
./docker/build.static.sh
```

The multi-stage image builds core and archives independently, rejects overlapping
output paths, and exports one complete Hugo output tree to `public/`. Rsync that
directory to the server directory corresponding to `/docs/`.

Docker reuses the archive stage when only active documentation changes. Changes to
shared templates invalidate both affected stages, as required.

## Nginx runtime image

```sh
docker build -f docker/Dockerfile --build-arg HUGO_BASEURL=https://www.openriak.org/docs/ -t openriak-docs .
```

This final image contains the assembled site under the base URL path. Public
servers need only the exported static files; the runtime image is optional.
