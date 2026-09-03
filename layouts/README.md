# Layouts

- `docs-theme/` — shared product documentation theme.
- `homepage/` — homepage templates.
- `archive-technical-blog/` — archive templates and Markdown render hooks.
- `common-docs/` — shared Hugo data, header, and standard site-section layouts.
- `_vendor/` — vendored Hugo modules retained with the layout system.

## Product page features

Related pages use version-independent paths in front matter. Paths are resolved
within the current product and version, and a missing target stops the build:

```yaml
related:
  - page: 'reference/configuration'
    reason: 'Understand configuration-file precedence.'
  - page: 'reference/faq'
    title: 'Frequently asked questions'
```

Fenced code blocks automatically show their language and offer copy, line-number,
text-wrap, shell-command-split, and download actions. Line numbers are a display
option and are never included in copied or downloaded content. Text wrapping
uses the available content width without creating new numbered lines.

Line numbers, text wrapping, and shell-command splitting are remembered by code
language. Changing one block immediately applies that option to every block of
the same language, and the preference is reused on other pages and after a
refresh. The block used to change an option remains anchored at the same
viewport position while other matching blocks change height.

## Configuration reference shortcodes

Use `configuration-reference-table` to render a filtered collection of settings.
Use `configuration-reference-item` when a page needs the complete details for one
exact mapping name:

<pre><code>&#123;&#123;&lt; configuration-reference-item config-name="mdc.fullsync_interval.$cluster_name" &gt;&#125;&#125;</code></pre>

The item shortcode fails the Hugo build when `config-name` is missing or does not
match exactly one generated setting. Its default value follows the selected
operating system, and every configuration name, application name, option, and
explicit default has an appropriate copy control.

The **Split command** action is shown for `bash`, `shell`, and `sh` blocks. It
uses quote-aware tokenisation to split a command at option boundaries and adds
shell continuation characters. It is separate from ordinary text wrapping.
Ordinary wrapping may be enabled at the same time to wrap unusually long split
lines to the available width. Split lines receive their own sequential line
numbers, and Bash comments retain comment styling. While Split command is
enabled, both Copy and Download use the transformed shell script.

Download filenames use these optional code-fence attributes:

- `filename` supplies the complete filename stem without a page prefix.
- `partialname` replaces the default one-based code-block number in the
  generated `{product}-{version}-{page}-{partialname}` stem.
- `extension` overrides the extension inferred from the fence language. Write
  it without the leading dot. Common defaults include `txt` for `text`, `conf`
  for `conf`, `erl` for `erlang`, `.advanced.config` for `advancedconfig`, and
  `sh` for `bash`, `shell`, or `sh`. `advancedconfig` blocks use Erlang syntax
  highlighting. An explicit `extension` requires a language before the
  attribute block; this keeps legacy filename-style fences such as
  ```` ```/etc/riak.conf ```` compatible.

The inferred or explicit extension is always appended to the stem. For example:

````markdown
```text {filename="riak.conf"}
storage_backend = bitcask
```

```conf {filename="riak"}
storage_backend = bitcask
```

```erlang {filename="riak"}
application:set_env(riak_core, ring_creation_size, 64).
```

```erlang {partialname="schedule-fullsync"}
application:set_env(riak_repl, fullsync_interval, 360).
```

```bash {partialname="start-riak"}
riak start --config /etc/riak/riak.conf
```
````

These produce `riak.conf.txt`, `riak.conf`, `riak.erl`,
`openriak-kv-3.4.0-configure-fullsync-replication-schedule-fullsync.erl`, and
`openriak-kv-3.4.0-openriak-cli-commands-start-riak.sh` on the example pages.
Without `filename` or `partialname`, the final stem component is the code
block's one-based position on the page.

Product and page components are automatically converted to portable URL-style
filename components. Author-supplied `filename`, `partialname`, and `extension`
values must already be valid on Linux and Windows. Hugo stops the build for
control characters, `< > : " / \\ | ? *`, trailing spaces or dots, or Windows
device names such as `CON`, `NUL`, `COM1`, and `LPT1`.

The version-mount generator compares effective Markdown pages across releases
and writes page status data under `tools/generated/page-provenance/`. Product
pages use it to label pages as new, updated, or last changed in an earlier version.
