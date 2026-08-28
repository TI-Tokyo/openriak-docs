---
title: 'Custom code constraints'
description: 'Define the names, fields, states, limits, and version applicability for custom code constraints.'
weight: 2
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\custom-code.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/ObjectAPI.html#commit-hooks'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Define the names, fields, states, limits, and version applicability for custom code constraints.

## Details

### Installing Custom Code

Riak supports the use of Erlang named functions in compiled modules for
[pre/post-commit hooks]({{< baseurl >}}kv/3.4.0/how-to/develop/write-commit-hook/), and MapReduce operations. This
doc contains installation steps with simple examples for each use case.

Your developers can compile [custom erlang code]({{< baseurl >}}kv/3.4.0/how-to/develop/write-commit-hook/), which
they can send to you as a *beam* file. You should note that in Erlang, a file
name must have the same name the module. So if you are given a file named
`validate_json.beam`, do not rename it.

> *Note: The [Configure](#configure) step (`add_paths`) also applies to installing JavaScript files.*

#### Compiling

If you have been given Erlang code and are expected to compile it for
your developers, keep the following notes in mind.

**Note on the Erlang Compiler**
You must use the Erlang compiler (`erlc`) associated with the Riak
installation or the version of Erlang used when compiling Riak from source.
For packaged Riak installations, you can consult Table 1 below for the default
location of OpenRiak's `erlc` for each supported platform. If you compiled from
source, use the `erlc` from the Erlang version you used to compile Riak.

<table style="width: 100%; border-spacing: 0px;">
<tbody>
<tr align="left" valign="top">
<td style="padding: 15px; margin: 15px; border-width: 1px 0 1px 0; border-style: solid;"><strong>CentOS &amp; RHEL Linux</strong></td>
<td style="padding: 15px; margin: 15px; border-width: 1px 0 1px 0; border-style: solid;">
<p><tt>/usr/lib64/riak/erts-5.9.1/bin/erlc</tt></p>
</td>
</tr>
<tr align="left" valign="top">
<td style="padding: 15px; margin: 15px; border-width: 1px 0 1px 0; border-style: solid;"><strong>Debian &amp; Ubuntu Linux</strong></td>
<td style="padding: 15px; margin: 15px; border-width: 1px 0 1px 0; border-style: solid;">
<p><tt>/usr/lib/riak/erts-5.9.1/bin/erlc</tt></p>
</td>
</tr>
<tr align="left" valign="top">
<td style="padding: 15px; margin: 15px; border-width: 1px 0 1px 0; border-style: solid;"><strong>FreeBSD</strong></td>
<td style="padding: 15px; margin: 15px; border-width: 1px 0 1px 0; border-style: solid;">
<p><tt>/usr/local/lib/riak/erts-5.9.1/bin/erlc</tt></p>
</td>
</tr>
<tr align="left" valign="top">
<td style="padding: 15px; margin: 15px; border-width: 1px 0 1px 0; border-style: solid;"><strong>SmartOS</strong></td>
<td style="padding: 15px; margin: 15px; border-width: 1px 0 1px 0; border-style: solid;">
<p><tt>/opt/local/lib/riak/erts-5.9.1/bin/erlc</tt></p>
</td>
</tr>
<tr align="left" valign="top">
<td style="padding: 15px; margin: 15px; border-width: 1px 0 1px 0; border-style: solid;"><strong>Solaris 10</strong></td>
<td style="padding: 15px; margin: 15px; border-width: 1px 0 1px 0; border-style: solid;">
<p><tt>/opt/riak/lib/erts-5.9.1/bin/erlc</tt></p>
</td>
</tr>
</tbody>
</table>

Table 1: Erlang compiler executable location for packaged Riak installations
         on supported platforms

Compiling the module is a straightforward process.

```text
erlc validate_json.erl
```

Next, you'll need to define a path from which compiled modules can be stored
and loaded. For our example, we'll use a temporary directory `/tmp/beams`,
but you should choose a directory for production functions based on your
own requirements such that they will be available where and when needed.

**Note:**
Ensure that the directory chosen above can be read by the `riak` user.

Successful compilation will result in a new `.beam` file,
`validate_json.beam`.

#### Configure

Take the `validate_json.beam` and copy this file to the `/tmp/beams` directory.

```text
cp validate_json.beam /tmp/beams/
```

After copying the compiled module into `/tmp/beams/`, you must update
`app.config` and configure Riak to allow loading of compiled modules from
the directory where they're stored (again in our example case, `/tmp/beams`).

Edit `app.config` and insert an `add_paths` setting into the `riak_kv`
section as shown:

```erlang
{riak_kv, [
  %% ...
  {add_paths, ["/tmp/beams/"]},
  %% ...
```

After updating `app.config`, Riak must be restarted. In production cases, you
should ensure that if you are adding configuration changes to multiple nodes,
that you do so in a rolling fashion, taking time to ensure that the Riak key
value store has fully initialized and become available for use.

This is done with the `riak admin wait-for-service` command as detailed
in the [Commands documentation]({{< baseurl >}}kv/3.4.0/reference/commands/riak-admin/#wait-for-service).

**Note:**
It is important that you ensure riak_kv is active before restarting the next
node.

#### Commit Hooks

For store requests it is possible, via bucket properties, to configure "commit hooks" - functions that will be applied either pre-commit (before the PUT has coordinated), or post-commit (after coordination and before response to the client).  This may have uses such as: value validation; updating inverted index objects; triggering actions in external systems.

Commit hooks are an expert feature, and should not be added without an understanding of the Riak codebase.
