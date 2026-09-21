# KV CLI metadata, schema 1

Generated as `kv/VERSION/cli-commands.json` in the metadata stage; `deploy` copies
it to `content/openriak-kv/metadata/VERSION/cli-commands.json`. The generator
preserves deterministic ordering; generation dates are the staged file mtimes,
as displayed by `list`.

## Document

| Field | Meaning |
| --- | --- |
| `schema_version` | Integer `1`. |
| `product`, `version` | `kv` and the selected exact release. |
| `status`, `warnings` | `complete` or `partial`, with discovery gaps. Partial documents cannot be deployed. |
| `source` | Root repository, `riak-VERSION` ref and resolved commit. |
| `repositories` | Resolved source dependency identities and commits. |
| `runtime` | Image tag, immutable ID, digests, version label, installed package version, OTP and OS evidence. |
| `commands` | Array of command records below, ordered by stable ID. |
| `service_variants` | OS family and service-manager variants for lifecycle actions. |
| `argument_types` | Exact Erlang type declarations indexed by module. |
| `coverage` | Registration results, inspected scripts, auxiliary roles, documentation checks and attach resolution results. |
| `working_directory` | Present only with `--keep-workdir`; a local diagnostic path. |

`complete` describes coverage of the recorded scope. It does not imply that a
command was executed successfully. Known unavailable commands and historical
examples absent from the selected release can occur in a complete inventory.
Uninspected executables, failed registration or unavailable implementation/type
information required for discovery instead produce warnings and a partial result.

## Command record

| Field | Meaning |
| --- | --- |
| `id` | Stable identifier, e.g. `shell:riak admin cluster join` or `erlang:riak_client:aae_fold/2:erase_keys`. |
| `path` | Token hierarchy. Erlang function entries sit beneath `riak attach` for grouping. |
| `invocation` | Shell invocation, Erlang function/arity, or explicitly marked argument template. |
| `context` | `shell` or `erlang`. Never run an Erlang expression as a shell command. |
| `kind` | `clique`, `shell`, `command_group`, `console_dispatch`, `auxiliary`, `erlang_function`, or `erlang_subcommand`. |
| `availability` | `available`, `unavailable`, `removed`, or `help_only`. `unavailable_reason` explains missing handlers. |
| `deprecated`, `removed`, `hidden` | Boolean annotations. Helpers are hidden from the main command list by default. |
| `visibility` | Erlang exports annotated `@private` are `internal`; other Erlang exports are `public`. Internal exports also have `hidden: true`. |
| `aliases` | Alternate invocations, each with its own `deprecated` boolean. Alias spellings may also have records of their own. |
| `arguments` | Clique key specs, usage placeholders, ordered Erlang argument positions, or the string `unrestricted` for an unrestricted Clique key spec. |
| `argument_format` | `key=value` for Clique commands; other contexts use signatures and usage forms. |
| `options`, `global_options` | Flag declarations; optional attributes include short form, datatype, callback validators/typecasts, value placeholder, description, source and hidden flag. |
| `help`, `help_status` | Extracted text and `available` or `not_provided`. Static help can contain unresolved shell variables/Erlang format placeholders. |
| `help_sources`, `usage` | Help evidence and extracted usage lines. |
| `provenance` | Runtime script/BEAM hashes, registration callback, and/or Git source locations. |
| `subcommands` | IDs of immediate children. |
| `variants` | Applicable lifecycle service variants. |
| `dispatch_source`, `handlers` | Shell branch and reachable console-function evidence for auditing legacy argument processing. |
| `documentation_examples` | Historical shell examples, where matched, with source page and line. |

Clique flags use their shell spelling (`--node`, `-n`); their `key` retains the
registry identifier. Auxiliary getopt declarations use the same flag spelling. Flags extracted from help/dispatch have a `source` annotation. Consumers
should deduplicate equivalent spellings when combining these sources and must
not infer requiredness from the absence of a default. An empty flag list means
no flags were extracted, not a promise that every argument will be rejected.
`wildcard_path: true` identifies registered variable path tokens such as `*`.
Clique's executable placeholder `_` in configuration commands is normalized to
`riak admin`, including its usage text. The `riak-admin` spelling is an alias.

Erlang records additionally carry `module`, `function`, `arity`, `signatures`,
`specifications`, `implementation`, `prerequisites`, and `examples`. AAE child
records have a `selector`, query-specific type signatures, and
`invocation_is_template: true`; the ellipsis must be replaced with actual
arguments. `argument_types` retains nested filters, enums and change-method
unions for the reference renderer. Historical examples are not rewritten
or executed, and may contain historical errors.

The attach scope is the exported `riak`/`riak_client` API plus documented calls
in other Riak modules. It excludes arbitrary Erlang/OTP expressions, internal
module exports unrelated to these entry points, and dynamically loaded plugins
not shipped in the selected image.

## Service variants

Each variant has `action` (`start`, `stop`, `restart`, `status`), `os_families`,
`service_manager`, `invocation`, `requires`, and `provenance`. Service-backed
variants also retain the release's `service_definition`. Match both OS family
and service manager/context: an Alpine container without OpenRC should use the
direct variant, not assume OpenRC is running. The `*` OS family denotes direct
launcher commands. Native service forms are derived from release packaging;
the inventory probe does not start every OS's init system.
