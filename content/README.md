# Content

`hugo.yaml` defines one Hugo project containing four page families:

- `portal/` — the homepage.
- `community/` — standard authored pages, beginning with the Community landing page.
- `openriak-kv/`, `openriak-cs/`, and `openriak-ts/` — instances of the shared product page family.
- `archive-technical-blog/` — the paginated blog page family.

Shared and site-specific web assets live under `static/`.

Everything under `content/` is user-maintained source. Build tools must not create or modify files here; generated Hugo inputs belong under `tools/generated/`.
