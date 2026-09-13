# OpenRiak Docker has moved

The runtime-image tool is maintained in
[TI-Tokyo/openriak-docker](https://github.com/TI-Tokyo/openriak-docker), with shared
infrastructure in [TI-Tokyo/openriak-tooling](https://github.com/TI-Tokyo/openriak-tooling).
This directory contains compatibility launchers only.

Clone both repositories beside openriak-docs and run `python3 scripts/setup.py`
in openriak-docker. Existing launcher commands forward to that checkout;
`OPENRIAK_DOCKER_ROOT` overrides its location.

Build/refresh and registry push operate in the tool repository. To update this
site, run an explicit publication from that repository:

```sh
./openriak-docker publish --version 3.4.1 --namespace tiotjp \
  --docs-root ../openriak-docs --whatif
```

Remove `--whatif` to apply the verified export locally. No Git commit/push or
site deployment is performed. Published downloads, records and metadata remain
owned by this repository. The original implementation remains in Git history.
