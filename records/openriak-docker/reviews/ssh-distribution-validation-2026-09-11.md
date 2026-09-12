# SSH distribution validation — 2026-09-11

Added `distribute add-node`, `list-nodes`, `check-nodes`, `start`, `monitor`,
`logs` and `fetch`. The portable plan/run/collect workflow remains available.

Validation command:

```sh
python3 tools/openriak-docker/tests/run_without_docker.py
```

**260 tests passed**, including the existing 640 generated-artifact comparisons.
The guard rejects direct Docker, Skopeo, SSH and SCP calls during the unit suite.

SSH-specific checks cover:

- Node persistence, key paths without key contents, file permissions and explicit replacement.
- Noninteractive SSH login/exit, strict host-key checking and remote shell quoting.
- Node-count checks, SCP staging and reconnection after a lost launch response.
- Retaining the exact source bundle across partial launch retries.
- Actual local `nohup`/`ps` execution of a tiny fake worker that writes a receipt.
- PID reuse and receipts from an unexpected manually restarted process.
- Monitoring without treating connection failures as completion.
- Automatic retrieval of stopped workers, including failure logs.
- Interrupted transfers, receipt changes during transfer and resuming after local promotion.
- Passed artifact/OCI archive hashes and collection of fetched approvals.
- SSH `tail -f` construction and stopping the viewer without stopping builds.
- Rejecting archive traversal and unsafe remote working paths.

No actual SSH node was contacted, and no image was built, container started or
registry updated. The local fake worker performs no OpenRiak or Docker work.
Actual authentication, remote Docker access and multi-machine transfers remain
to be verified on the user's configured machines.

## Native local worker extension

Added `add-node NAME --local --workdir PATH` for WSL2 and other local Linux
workers without an SSH server or key. Local workers share the existing launch,
PID identity, receipt and artifact validation protocol, using direct subprocesses
and file copies. Existing SSH node records remain compatible.

**264 tests passed** after this extension. Added coverage for local registration
and prerequisite checks, rejecting mixed local/SSH settings and duplicate local
workers, and a full local stage/launch/monitor/fetch/log workflow with a fake
worker. The test used no SSH/SCP connections, Docker builds or containers. The
640 generated-artifact comparisons continue to pass.

## Managed run command

`distribute run --plan FILE` now launches every selected local/SSH worker with
nohup. `start` is an alias; the individual executor is named `worker`. Default
retrieved output uses `PLAN.results/NODE/`, while worker-side folders include the
plan filename, node name and deployment ID. Existing deployments retain saved
paths. `--output ROOT` overrides the retrieved results root.

**266 tests passed**, including mixed local/SSH dispatch through `run`, default
and overridden output paths, command aliases, named result directories, legacy
deployment retrieval and the generated-artifact baseline. Actual builds and SSH
connections were not run.
