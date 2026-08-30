# Content

`hugo.yaml` defines one Hugo project containing four page families:

- `homepage/` — the homepage.
- `community/` — standard authored pages, beginning with the Community landing page.
- `riak-kv/{version}/` — Riak KV sources from 2.0.0 up to, but not including, 3.4.0. They publish at the existing `openriak-kv/{version}` URLs.
- `openriak-kv/{version}/` — OpenRiak KV sources beginning at 3.4.0.
- `openriak-cs/{version}/` and `openriak-ts/{version}/` — versioned instances of the shared product page family.
- `archive-technical-blog/` — the paginated blog page family.

Shared and site-specific web assets live under `static/`.

Each direct semantic-version directory is a cumulative content layer over
earlier versions in that same source product. Everything under `content/` is
user-maintained source. Build tools must not create or modify files here;
generated Hugo inputs belong under `tools/generated/`.
