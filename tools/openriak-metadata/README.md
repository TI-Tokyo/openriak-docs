# OpenRiak release metadata generator

`openriak-metadata` generates deterministic package, operating-system, and
configuration-default metadata for exact OpenRiak releases. It requires Linux,
Python 3.11 or newer, Git, and unauthenticated HTTPS access to `files.tiot.jp`
and GitHub.

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

The files are written beneath `out/kv/3.4.1/`. `packages` and `defaults`
subcommands are available for development. Every subcommand accepts
`--cache-dir`, `--refresh`, `--strict`, `--keep-workdir`, and `--log-level`.

KV defaults are extracted from the exact `riak-VERSION` tag and its recursive
locked Erlang dependencies. CS and TS currently generate package metadata plus
a `defaults.json` document whose status is `not_implemented`.

Run the offline fixture suite with:

```sh
(cd tools/openriak-metadata && python3 -m unittest discover -s tests -v)
```
