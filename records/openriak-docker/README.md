# Retained OpenRiak KV Docker evidence

These files belong in Git. Local execution files belong in `.work/openriak-docker/`.

- `images/`: image approvals, platform tests and normalized push/Scout evidence.
- `bases/`: reusable-base approvals and publication evidence.
- `experiments/`: retained prototype reports.
- `distributed/`: frozen portable plans and received worker reports.
- `reviews/`: human-written investigation and validation reports.
- `migrations/`: relocation receipts and verification results.

A `current.json` index maps logical report filenames to immutable, SHA-256-addressed
`history/*.json` snapshots. Each historical run has its own directory and index.
Use the tool or the documentation readers to resolve and verify these pointers.
Do not edit the generated snapshots. CVE assessments remain editable Markdown
under `content/openriak-kv/docker/`.

Approved source files are stored separately in `artifacts/openriak-docker/`.
OCI archives, original Scout payloads and diagnostic logs remain local under
Git-ignored `.work/openriak-docker/`. Cleanup retains 90 days by default;
`cleanup --clear-archives --delete` removes all local archives regardless of age.
These durable records and the approved source files remain separate and retained.

See [the tool README](../../tools/openriak-docker/README.md) for commands and cleanup boundaries.
