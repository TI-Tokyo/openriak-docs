# OpenRiak release metadata generator

`openriak-metadata` generates deterministic package, operating-system, and
configuration-default metadata for exact OpenRiak releases. It requires Linux,
Python 3.11 or newer, Git, and unauthenticated HTTPS access to `files.tiot.jp`
and GitHub.

To refresh the documentation repository's package listings directly, run this
from the repository root:

```sh
tools/openriak-metadata/openriak-metadata packages \
  --product kv \
  --version 3.4.0 --version 3.4.1 \
  --refresh --update-repo
```

`--version` is repeatable on every subcommand. Duplicate versions are processed
only once. `packages --update-repo` handles staging and copying automatically:
it discovers packages and computes their checksums for every requested version,
then installs `supported-os.json` and `downloads.json` beneath
`content/openriak-kv/metadata/{version}/`. Configuration defaults, OS aliases,
other versions, and Docker test caches are left untouched.

Repository updates require complete metadata for **every** requested version,
even without `--strict`. No matching packages, download failures, or discovery
warnings prevent the entire batch from being installed. Existing files remain
unchanged during discovery. Installation prepares all replacements and backups,
replaces each file atomically, and rolls back earlier replacements if an
installation error occurs. Identical files are not rewritten.

`--update-repo` is available on `packages` and is mutually exclusive with
`--output`. The repository wrapper defaults to its own checkout. Use
`--update-repo /path/to/openriak-docs` to select another checkout or when using
an installed copy of the CLI. It updates authoritative package metadata only;
it does not build Docker images or restart a development server. To reload the
Docker-hosted preview's package metadata afterward:

```sh
docker compose -f docker/compose.yaml restart core
```

Install it from the repository root:

```sh
python3 -m pip install ./tools/openriak-metadata
```

Generate all metadata:

```sh
openriak-metadata generate \
  --product kv \
  --version 3.4.1 \
  --output ./out
```

The files are written beneath `out/kv/3.4.1/`. Repeat `--version` to generate
additional releases beneath the same output directory. `packages` and `defaults`
subcommands are available for development. Every subcommand accepts
`--cache-dir`, `--refresh`, `--strict`, `--keep-workdir`, and `--log-level`.
Package generation streams every discovered package through SHA-256 and writes
the digest into `downloads.json`; package bodies are not retained. Four files
are hashed concurrently by default. Use `--checksum-workers` to tune that limit.
Digests are cached by URL beneath the metadata cache, so interrupted and repeat
runs do not download packages again unless `--refresh` is supplied.

For releases whose documentation does not consume generated configuration
defaults, generate only supported operating systems and downloads:

```sh
openriak-metadata generate \
  --product kv \
  --version 3.2.5 \
  --output ./out \
  --skip-defaults
```

This writes `supported-os.json` and `downloads.json` without resolving source
repositories or creating `defaults.json`.

KV defaults are extracted from the exact `riak-VERSION` tag and its recursive
locked Erlang dependencies. CS and TS currently generate package metadata plus
a `defaults.json` document whose status is `not_implemented`.

Run the offline fixture suite with:

```sh
(cd tools/openriak-metadata && python3 -m unittest discover -s tests -v)
```
