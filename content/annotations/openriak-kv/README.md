# CLI documentation annotations

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
the same merge rules. The initial recipes cover `describe`, `member-status`,
`riak_client:get/3`, and shared `riak admin` connection errors; remaining topics
are tracked by the coverage reports.

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
The page also exposes its findings under **Reference sources → Syntax differences
requiring manual review**. Original help remains in **Help text**.

Review an entry against the command implementation or a focused runtime scenario.
Correct missing structured fields in the metadata generator or add an appropriate
command annotation, then regenerate this report. A `# Syntax` override remains
available and is itself noted for review; it does not suppress the comparison.
Generation never rewrites the deployed CLI source JSON.
