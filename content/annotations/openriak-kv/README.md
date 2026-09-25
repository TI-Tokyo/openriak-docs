# CLI and settings documentation annotations

Edit command-specific Markdown here. The merge order is generated metadata,
`common.md`, then `VERSION.md` in the same command directory. For example:

```
cli/riak/admin/describe/common.md
cli/riak/admin/describe/3.4.0.md
cli/riak/admin/member-status/common.md
cli/riak/admin/common.md
riak-attach/riak_client/get/common.md
```

A version file is optional. Omitted sections and fields inherit the earlier
layer. The directory identifies the command. For an Erlang operation with
multiple arities, use `# Metadata` with `command: erlang:riak_client:get/3` to
select the arity whose examples and evidence you are annotating. Shared command
errors belong on the common ancestor; descendant pages link to them.
Erlang pages also link to shared connection and shell errors on `riak attach`.
Describe common Erlang parameters in `# Shared arguments` on a module parent
(for example, `riak-attach/riak_client/common.md`) or an operation parent such
as `riak_client/aae_fold/common.md`. Use the same entry format as `# Arguments`.
Children retain their own types and requiredness, and link their parameter
descriptions to the nearest parent defining that name. Use distinct names for
different meanings: `Client` is a Riak handle; `Recipient` is a process ID.
For AAE selectors, use `riak-attach/riak_client/aae_fold/SELECTOR/common.md`
with a command ID such as `erlang:riak_client:aae_fold/1:object_stats`.

These files are build inputs, not Hugo pages. They are not mounted into public
content and do not require Hugo front matter.

## Format

Use `#` for sections, `##` for named entries, and `###` for long fields.
Descriptions are ordinary Markdown, including multiple paragraphs, lists, links,
and fenced code. Structural headings inside fenced code are preserved as code.
Use level 4 or deeper for headings within an entry's long field.

```markdown
# Summary

Read the schema documentation for configuration settings.

# Description

Supply setting names, such as `ring_size`.

Use `riak admin show` to read current values.

# Arguments

## variable

required: true
repeatable: true
datatype: configuration setting name

### Description

One or more names, separated by spaces.

Do not supply a `name=value` assignment.

# Options

## --format

required: false
repeatable: false
default: human

### Valid values

- human
- csv
- json

### Description

Select the output writer.

CSV only renders tables; it omits this command's descriptions.

# Examples

## describe:format-json

title: As JSON

### Description

Read the description as JSON text records.

The launcher appends an `ok` line after the JSON.
```

Supported sections:

- **Metadata:** optional `command` and comma-separated exact `versions`.
- **Summary:** one sentence describing the command.
- **Syntax:** optional Markdown replacing generated syntax, including code
  blocks for multiple forms. Usually inherit the discovered syntax.
- **Arguments:** replaces the argument list; each `## name` has `datatype`,
  `required`, `repeatable`, `default`, `### Valid values` (bullet list), and
  `### Description`. Required/repeatable accept `true` or `false`. Leave unknown
  fields out rather than inventing a value. Version-specific argument sections
  also replace the list, so include every argument you want displayed.
- **Options:** patches generated options by their displayed flag name, such as
  `--format` or `-f`. Fields are the same as arguments. Omitted fields inherit.
  Unknown flags fail the merge.
  Set `omit: true` to suppress a falsely discovered flag, for example a flag
  mentioned in a parent's help that actually belongs to a child. Original help
  and source metadata remain available for review. A version file can restore
  the flag with `omit: false`.
- **Description:** longer explanation of the command's behaviour.
- **Notes:** Markdown; an empty section clears inherited notes.
- **Examples:** patches generated examples by stable ID. Use `title`, optional
  `outcome` (`success` or `error`), and long fields `### Description`,
  `### Prerequisites`, `### Invocation`, `### Expected output`. New examples
  require invocation and description. An empty section clears examples.
- **Errors:** patches errors by stable ID; long fields are `### Condition`,
  `### Description`, and `### Remedy`. New errors require all three fields.
  An empty section clears command-specific errors, while ancestor error links
  remain available.
- **Results:** optional complete replacement of expected-result entries, using
  `## ID` and `### Description`. Rendered within Description.
- **Related documentation:** Markdown links appended before generated related
  links. Paths resolve relative to the rendered command page, not this file.
- **Tags:** feature, repository, module and concept lists; see Shared tags below.
- **Reviewed against:** exact versions mapped to review fingerprints.

Use separate paragraphs under a long-field heading rather than embedding `\n`
escapes in a key-value line. Invocation and expected-output fields may contain
one fenced code block; its fence is removed before rendering.

## Evidence, review, and preview

Captured stdout, stderr, exit status, and test provenance are immutable. An
edited invocation no longer displays the old observation as its output.
Original evidence remains under **Reference sources**. Test dates are displayed
as YYYY-MM-DD; the original timestamp is retained in the metadata.

`Reviewed against` hashes cover command definitions and scenario contracts.
They ignore output timestamps. Review the changed contract before updating a
hash. Completeness and stale-review reports are in
`tools/generated/openriak-kv/cli-coverage/VERSION.json`.

```sh
node tools/scripts/watch-cli-reference.js --once
```

The Docker preview watches this directory recursively. Editing a Markdown file
updates the preview without rerunning Docker scenarios. Invalid edits retain
the last valid preview and log an error. Full metadata synchronization applies
the same merge rules. Every CLI topic in 3.4.0 and 3.4.1 has annotations, including
Erlang client APIs, AAE selectors, replication queues and launcher helpers.
Runtime recipes live in `../openriak-metadata/scenarios/`; their assertions and
observations are deployed with the CLI JSON. Source-based examples for interactive
terminals, upgrades and operations needing a larger topology do not carry a
Docker verification badge. A tested rejection does not establish a successful
operation. Version files explain known runtime differences.

## Generated syntax and manual review

Syntax is assembled by the docs adapter from the discovered command tree and
structured parameters after applying annotations. Subcommand choices link to
their own reference pages. Parent alternatives exclude unavailable commands;
usage-derived flags on a parent are not promoted to global options because they
may belong to a child command. Erlang forms use the discovered function heads
and selector expressions.

Leaf forms use argument names, key=value declarations, required/repeatable flags,
option aliases and recorded values. Clique's global help flag gets its own form
because it can be used without executing the command or supplying its arguments.
When the metadata cannot establish ordering, grouping, requiredness or option
value arity, the page retains the supplied usage. Incomplete generated candidates
are only shown in the review material, not as recommended invocations.

Each synchronization and preview refresh writes:

- `tools/generated/openriak-kv/cli-syntax-review/VERSION.md`: readable review queue.
- `tools/generated/openriak-kv/cli-syntax-review/VERSION.json`: the same findings
  in structured form, including topics that matched.

Each entry includes generated candidates, supplied syntax, the displayed source,
missing/extra subcommands, and any uncertainty. Whitespace and the documented
`riak-admin` spelling are normalized. Other differences are flagged conservatively,
so a finding can be a notation difference rather than an implementation error.
Explicitly discovered command aliases are compared using their canonical spelling.
Where both hyphens and underscores are accepted, the hyphenated command is used
in Syntax and underscore aliases remain under Alternate spellings. This applies
to command prefixes only: argument values, option names and Erlang function names
are not rewritten. Original usage remains intact in Help text and review reports.
The page also exposes its findings under **Reference sources → Syntax differences
requiring manual review**. Original help remains in **Help text**.

Review an entry against the command implementation or a focused runtime scenario.
Correct missing structured fields in the metadata generator or add an appropriate
command annotation, then regenerate this report. A `# Syntax` override remains
available and is itself noted for review; it does not suppress the comparison.
Generation never rewrites the deployed CLI source JSON.

## User scenarios and test details

Each example should name a situation an operator encounters, briefly explain why
the command helps, and describe the expected outcome. Put environment setup,
Docker details, fixture creation and test assertions in the generated evidence,
not in the visible explanation. Use a Markdown example-description override to
improve wording without changing captured output.

Verified examples show their output separately from a collapsed **Tested on…**
section at the bottom of the example. That section contains the runtime image,
recipe and case identifiers, test environment, and matching setup, execution and
verification steps. Its date uses YYYY-MM-DD. The evidence is immutable; editorial
overrides cannot replace test output or attach evidence to a changed invocation.

## Settings annotations

The same docs-owned layering applies to configuration settings in both 3.4.0
and 3.4.1. Edit `settings/SETTING/common.md`, optionally followed by
`settings/SETTING/VERSION.md`. Use the exact public configuration key as the
folder name, including dots and placeholders such as `$name`. Each of the 641
settings has a description and categorized tags. These files are not Hugo pages
and do not modify the deployed metadata or the openriak-metadata repository.

The catalogue includes 214 application-environment entries tagged
`secretSettings` in the metadata. Their annotations explain the source consumers
and link to the reviewed dependency revisions. These entries include internal
registries, runtime state, test fixtures and deprecated options as well as tuning
settings; discovery does not imply a `riak.conf` mapping. Version annotations
identify entries found only in a newer transitive dependency scanned for 3.4.0,
and explain the release-specific full-sync range representation.

For example, `settings/tictacaae_maxresults/common.md` can contain:

```markdown
# Description

Maximum differing tree leaves compared in one Tictac AAE exchange.
Smaller exchanges shorten each clock-comparison query.

# Tags

feature: tictac-aae
repository: riak_kv
module: riak_kv_vnode
concept: replica-repair

# Notes

Review this together with the range multiplier and repair-loop count.
```

Supported setting sections:

- **Description**, **Notes**, **Examples**, **Related documentation**: Markdown.
  The latter three appear on setting details; Description also appears in tables.
- **Application name**: displayed internal Erlang target.
- **Areas**: bullet list replacing the repository-area classification used by
  the table shortcode's `area` argument.
- **Datatype**: displayed type label, for example `Integer`.
- **Allowed values**, **Units**, **Constraints**: bullet lists replacing the
  corresponding displayed datatype fields. Constraints can contain Markdown.
- **Inferred default**: Markdown explaining a source fallback, application
  startup default, runtime calculation, or the absence of a default. Displayed
  as **Inferred from source** in the default column, separately from any generated
  OS default. An empty section clears the inherited inference.
- **Tags**: categorized lists, as described below.
- **Reviewed against**: exact versions and SHA-256 review fingerprints.

Omitted sections inherit; an empty section clears its inherited value. Datatype
fields and tag categories merge independently, so a version can replace allowed
values or concept tags while retaining the other categories. Setting names and
OS-specific default values cannot be overridden. Unknown sections, invalid tags,
and annotations targeting missing settings fail validation.

For `secretSettings`, datatype and value constraints are inferred from source
guards, type specifications and consumers. Enumerations list literal Erlang
values; open ranges, callback contracts and tuple shapes belong in Constraints.
Expected ranges are not necessarily checked by the application environment read.
For schema union datatypes, tables and details show one bullet per alternative.
Literal atoms, enum members and fixed numbers have copy controls; unrestricted
types such as Integer or Duration (ms) are plain text. A typed literal such as
`{atom, unlimited}` contributes only `unlimited`, and a union's bare `flag`
contributes `on` and `off`. An annotation's Allowed values section replaces the
alternatives with literal values. Validator corrections belong in Constraints
and should cite the reviewed schema implementation.
Inferred defaults distinguish read-site fallbacks from `.app.src` defaults and
runtime state. Source links identify the reviewed revisions; version annotations
handle release differences. These inferences do not change the original metadata
or its OS-specific defaults.

Changes to datatype labels, allowed values, units or constraints are recorded
with their old/new values and annotation filenames. Hugo emits non-failing
`WARN` entries for these corrections. An override equal to the inherited value
does not log a correction. Original metadata remains in the generated setting's
`source` field and in the detail display's **Reference sources** disclosure.

Review fingerprints cover each raw setting definition, excluding source line
numbers so a line-only move does not invalidate a review. The coverage and
stale-review report is written to
`tools/generated/openriak-kv/settings-coverage/VERSION.json`. Review an actual
contract change before updating a fingerprint. To compute the current hash:

```sh
node -e 'const {settingFingerprint} = require("./tools/scripts/settings-annotations"); const d = require("./content/openriak-kv/metadata/3.4.1/kv-settings.json"); console.log(settingFingerprint(d.settings.ring_size));'
```

The existing `node tools/scripts/watch-cli-reference.js --once` command now
regenerates both CLI and settings annotations, after the initial product metadata
synchronization. The Docker development preview watches both sets of files.
Valid edits, additions and removals refresh the data; invalid edits log an error
and preserve the last valid preview. Full synchronization uses the same merge.

## Shared tags

Settings, CLI commands and `riak attach` operations accept a **Tags** section:

```markdown
# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_replrtq_src
concept: cross-cluster-replication, queueing
```

Use these four category names, with comma-separated unique lowercase identifiers:

- **feature** identifies a subsystem or capability, such as `tictac-aae`,
  `leveled`, `cluster-management` or `queue-replication`.
- **repository** is the source repository name, such as `riak_core`.
- **module** is a source module confirmed by the command metadata or source
  configuration consumer. Where no consumer is identified, use the defining
  schema filename (for example `riak_kv.schema`); launcher-only commands can
  use their script name. A schema tag is not a claimed Erlang module.
- **concept** identifies shared concerns such as `replica-repair`, `memory`,
  `quorums`, `retention` or `concurrency`.

Reuse existing vocabulary when the meaning matches. Tags are editorial inputs,
not guessed at render time. Table text searches include the tags, and one filter
per category can be combined with the search. Filters use AND across categories;
select **All** to remove a category restriction, or **Clear filters** to clear the
query and every tag filter. CLI indexes support the same tag search and filters.

Settings tables also provide a **Metadata tag** filter populated from the raw
settings metadata, including `secretSettings`. These tags are searchable and
combine with the annotation category filters in the same way.

Setting details show all categories and up to eight related settings in the same
version. A candidate must share a feature and a concept; ranking gives each shared
feature three points and each shared concept one point, then sorts ties by name.
Source repository/module alone does not establish a relationship. Links target
stable anchors in the complete settings catalogue. Tables do not show related
settings. Names and defaults remain sourced from the unmodified release metadata.
