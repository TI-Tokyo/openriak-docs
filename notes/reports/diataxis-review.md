# OpenRiak KV Diátaxis review — 22 September 2026

The 3.4.0 baseline and 3.4.1 overlays now use the implemented paths in
[diataxis-page-map.json](diataxis-page-map.json): 40 Foundations topics, 148
How-to topics, 39 tutorial topics and 136 planned Reference topics. The command
catalogue expands the command topics into 279 generated pages for 3.4.0 and 286
for 3.4.1. Earlier unpublished paths have no new redirects.

Content has been reviewed for its Diátaxis purpose. Section introductions address
readers, procedural pages link to Foundations for concepts, related links appear
at the end, and connected learning/operational workflows have previous/next links.
Menus introduce basic topics before specialist operations. AWS EC2 sits below a
provider-specific cloud path so later Azure and OVHcloud exercises can sit beside
it. Heading levels now have size, spacing and border cues in addition to weight.

Settings/defaults, commands/help and package selections use the deployed JSON.
The learning environment uses the published Alpine 3.24 / OTP 26 Docker records.
Supplemental protocol definitions, backend callback signatures, metric aliases
and lookup tables live in versioned `kv-reference.json` files with pinned source
references. Hugo mounts these as data so edits refresh the development server.

## Checks completed

- Hugo v0.166.0 development-profile build, with drafts and `--panicOnWarning`:
  3,868 pages. Covers both OpenRiak versions, their inherited/alias routes, and
  the normal development-profile historical products.
- Rendered article-link and fragment audit: 1,403 modern-version pages, zero
  missing destinations or anchors.
- Diátaxis inventory, related/workflow link, CLI-key and API-table regression
  checks pass for 3.4.0 and 3.4.1.
- Architecture, version mounts, OS selection/defaults, metadata loading and
  synchronization, page provenance, CLI normalization and CLI-help tests pass.
- Command-page generation `--check` passes for both versions.
- Playwright checks against the user's server at port 1410 pass for reference
  filtering, regular-expression validation, sorting, workflow links,
  related links, heading distinctions and mobile width in both versions.
- The command-reference browser suite checks all 269 linked 3.4.0 topics,
  options/help, copying, service-manager variants, aliases, deprecation and
  unavailable status, Erlang arities, search indexing and mobile layout.
- Desktop/light and mobile/dark pages were visually inspected.

Reproduce the content checks with:

```sh
node --test tools/scripts/diataxis.test.js
node tools/scripts/generate-cli-pages.js --version 3.4.0 --check
node tools/scripts/generate-cli-pages.js --version 3.4.1 --check
python3 tools/scripts/check-diataxis-links.py PATH_TO_HUGO_OUTPUT
```

The browser tests need Playwright and a Chromium executable. The product-root
URL is configured with `OPENRIAK_DOCS_TEST_URL` for the Diátaxis suite; the CLI
suite uses `OPENRIAK_CLI_TEST_URL` for the command-index URL.

## Runtime verification

An isolated five-node 3.4.0 Alpine 3.24 / OTP 26 cluster exercised bucket-type
creation/activation; counters, sets, grow-only sets, maps and HyperLogLog; the
three-person index fixture; exact and projected queries; intersection, union and
subtraction; city-index grouped counts; and secondary-index pagination. Python,
Node.js and Java HTTP application examples passed read, update, index and delete
checks. Repeated increments deliberately change a counter and are not idempotent.

The following observations remain product/runtime work, rather than claims of
successful verification:

1. Query API pagination with a small `max_results` caused
   `riak_kv_query_server:handle_info/2` to call `hd([])` when a vnode returned an
   empty batch. The 3.4.0 HTTP request then timed out. The reference records the
   limitation, and the pagination tutorial uses the working secondary-index
   endpoint. Do not generalise this observation to untested releases/images.
2. Projected-city accumulation returned empty results on the tested image.
   Direct `city_bin` grouping returned `Osaka: 1, Tokyo: 2`; that is the exercise
   now used in the tutorial. Projected accumulation needs separate investigation.
3. The Alpine system `riak` wrapper altered quoted JSON arguments. The learning
   helper invokes the release launcher with the active generated VM arguments.
   The package wrapper needs a fix in its owning repository.

Native installations, AWS/Vagrant provisioning, complete recovery/replication/
security rehearsals, remaining language runtimes and 3.4.1 queued delivery have
not all been executed. These remain explicit To Do items. Partial settings
extraction warnings and unverified specialist integration compatibility remain
visible; no missing defaults or support guarantees have been invented.

The user's development server is retained. Only the isolated documentation test
cluster and temporary validation build containers are cleaned up.
