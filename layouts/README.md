# Layouts

- `docs-theme/` — shared product documentation theme.
- `homepage/` — homepage templates.
- `archive-technical-blog/` — archive templates and Markdown render hooks.
- `common-docs/` — shared Hugo data, header, and standard site-section layouts.
- `_vendor/` — vendored Hugo modules retained with the layout system.

## Product page features

Use `button-link` for a button-shaped link to another site page:

```markdown
{{% button-link link="[Downloads]" %}}Go to Downloads{{% /button-link %}}

[Downloads]: {{< product-version-root >}}downloads/
```

Use the `%` delimiters so Hugo renders the enclosed Markdown together with the
page. The `link` parameter accepts a reference alias in brackets or a URL.
Alternatively, omit `link` and put a complete Markdown link inside the shortcode.
Standard inline links, full reference aliases (`[Label][Alias]`), collapsed
references (`[Downloads][]`), and shortcut references (`[Downloads]`) all work.
Alias definitions may appear anywhere on the page and can include shortcodes
such as `product-version-root`. Wrap one link per shortcode. Destinations follow
normal Markdown link rules; this shortcode does not validate target pages.

The control is a normal same-tab link with a button border, a decorative
right arrow, and a visible keyboard focus ring. It supports the light and dark
themes and needs no JavaScript.

Set `indent` to move the link in from the left, and `padding` to control the space
inside its border. Both are optional; the defaults preserve the original appearance.

```markdown
{{% button-link link="[Downloads]" indent="1em" padding="small" %}}Go to Downloads{{% /button-link %}}
{{% button-link link="[Downloads]" padding="3em" %}}Go to Downloads{{% /button-link %}}
```

| Option | Value | Effect |
| --- | --- | --- |
| `indent` | `0` (default), or a CSS length such as `1em` | Left margin around the link container. |
| `padding` | `small` | `.2rem` vertically, `.45rem` horizontally. |
| `padding` | `medium` | `.35rem` vertically, `.65rem` horizontally. |
| `padding` | `large` (default) | Original `.55rem` vertically, `.9rem` horizontally. |
| `padding` | A CSS length such as `3em` | The same padding on all four sides. |

Custom values must be non-negative lengths (for example `px`, `em`, `rem`, `%`,
or viewport units), or `0`. The link height follows its text and selected padding.

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

For a page changed in a maintenance release, add an `update-summary` front
matter value containing a short description of the change since the previous
version. The release's **What's Changed** page groups new and updated pages by
their immediate container path, creates a heading for every container with
changes, and orders containers and pages as they appear in the sidebar. The
product-version landing page and **What's Changed** itself are excluded. A
missing or blank value is displayed as “Updated content”. Set
`hide_provenance: true` only on pages, such as **What's Changed**, that must not
display their own provenance.

The draft-only **To Do** section is the first item in the version sidebar. It
contains **For Review** first, recommendations for the four documentation areas,
and a **Tests** subsection. These pages live in the 3.4.0 release baseline and
are inherited by later versions.

The **To Do → For Review** page uses `{{< for-review >}}` to list all pages in
the current product version, including section landing pages, grouped in the same
navigation order as **What's Changed**. Its columns are **Page**, **Last Reviewed**,
and **Status**. Status lists `draft`, `status`, `review_scope`, `editorial_review`,
`technical_review`, and `review-by`, one property per line with human-readable labels and
unchanged values. List values are comma-separated; missing metadata is labelled
`Not set`, except that missing or blank `review-by` values default to `Unassigned`.
Set `review-by: 'Name'` in a page's front matter to assign a reviewer; lists of
reviewers also work and can be filtered individually. The report excludes itself. It is inherited by
later versions and appears only when Hugo builds drafts (`--buildDrafts`).
Dropdown filters match individual property values, including individual items in
list-valued review scopes. Active filters are combined with AND. Selections are
remembered in the browser per product, including across version changes; an
unavailable saved value falls back to All. Empty groups are hidden, a count shows
the matching pages, and **Reset filters** restores All. Without JavaScript, the
complete report remains visible.
With the draft preview running and Playwright installed, run
`node tools/scripts/for-review.browser.test.cjs` to check filtering and persistence.
`OPENRIAK_REVIEW_TEST_URL` and `OPENRIAK_BROWSER_EXECUTABLE` can override the
report URL and Chromium binary.
