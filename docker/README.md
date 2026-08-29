# HTTP-only Docker preview

This wrapper restores the old local Docker workflow using Hugo 0.165.0 without the former Ruby, Rake, Sass, or CoffeeScript toolchain.

From the repository root, run one of:

```sh
sh ./docker/run.local.sh
```

```powershell
.\docker\run.local.ps1
```

The default preview URL is <http://localhost:1314/docs/>. The container binds only to `127.0.0.1`, serves plain HTTP, includes draft content, watches for source changes by polling, renders to memory, and mounts the project read-only.

Set `HUGO_BASEURL` before launching to use a different path, for example:

```sh
HUGO_BASEURL=http://localhost:1314/openriak-docs/ sh ./docker/run.local.sh
```

Pass Compose `up` options through the wrapper, for example `sh ./docker/run.local.sh --detach`. Stop a detached preview with:

```sh
docker compose -f ./docker/docker-compose.localhost-preview.yaml down
```
