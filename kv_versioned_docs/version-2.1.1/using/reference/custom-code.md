---
title: "Installing Custom Code"
sidebar_position: 111
sidebar_label: Installing Custom Code
pagination_label: "Installing Custom Code"
hide_table_of_contents: true
last_update:
  author: RiakDocs
  date: 2015-05-05
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


Riak supports the use of Erlang named functions in compiled modules for
[pre/post-commit hooks](./../../../developing/usage/commit-hooks), and MapReduce operations. This
doc contains installation steps with simple examples for each use case.

Your developers can compile [custom erlang code](./../../../developing/usage/commit-hooks), which
they can send to you as a *beam* file. You should note that in Erlang, a file
name must have the same name the module. So if you are given a file named
`validate_json.beam`, do not rename it.

> *Note: The [Configure](#configure) step (`add_paths`) also applies to installing JavaScript files.*

### Compiling

If you have been given Erlang code and are expected to compile it for
your developers, keep the following notes in mind.

<RiakDocsNote title="Note on the Erlang Compiler">
You must use the Erlang compiler (`erlc`) associated with the Riak
installation or the version of Erlang used when compiling Riak from source.
For packaged Riak installations, you can consult Table 1 below for the default
location of Riak's `erlc` for each supported platform. If you compiled from
source, use the `erlc` from the Erlang version you used to compile Riak.
</RiakDocsNote>

<table style={{width: '100%', borderSpacing: '0px'}}>
<tbody>
<tr align="left" valign="top">
<td style={{padding: '15px', margin: '15px', borderWidth: '1px 0 1px 0', borderStyle: 'solid'}}><strong>CentOS &amp; RHEL Linux</strong></td>
<td style={{padding: '15px', margin: '15px', borderWidth: '1px 0 1px 0', borderStyle: 'solid'}}>
<p><tt>/usr/lib64/riak/erts-5.9.1/bin/erlc</tt></p>
</td>
</tr>
<tr align="left" valign="top">
<td style={{padding: '15px', margin: '15px', borderWidth: '1px 0 1px 0', borderStyle: 'solid'}}><strong>Debian &amp; Ubuntu Linux</strong></td>
<td style={{padding: '15px', margin: '15px', borderWidth: '1px 0 1px 0', borderStyle: 'solid'}}>
<p><tt>/usr/lib/riak/erts-5.9.1/bin/erlc</tt></p>
</td>
</tr>
<tr align="left" valign="top">
<td style={{padding: '15px', margin: '15px', borderWidth: '1px 0 1px 0', borderStyle: 'solid'}}><strong>FreeBSD</strong></td>
<td style={{padding: '15px', margin: '15px', borderWidth: '1px 0 1px 0', borderStyle: 'solid'}}>
<p><tt>/usr/local/lib/riak/erts-5.9.1/bin/erlc</tt></p>
</td>
</tr>
<tr align="left" valign="top">
<td style={{padding: '15px', margin: '15px', borderWidth: '1px 0 1px 0', borderStyle: 'solid'}}><strong>SmartOS</strong></td>
<td style={{padding: '15px', margin: '15px', borderWidth: '1px 0 1px 0', borderStyle: 'solid'}}>
<p><tt>/opt/local/lib/riak/erts-5.9.1/bin/erlc</tt></p>
</td>
</tr>
<tr align="left" valign="top">
<td style={{padding: '15px', margin: '15px', borderWidth: '1px 0 1px 0', borderStyle: 'solid'}}><strong>Solaris 10</strong></td>
<td style={{padding: '15px', margin: '15px', borderWidth: '1px 0 1px 0', borderStyle: 'solid'}}>
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

<RiakDocsNote>
Ensure that the directory chosen above can be read by the `riak` user.
</RiakDocsNote>

Successful compilation will result in a new `.beam` file,
`validate_json.beam`.

### Configure

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

This is done with the `riak-admin wait-for-service` command as detailed
in the [Commands documentation](./../../admin/riak-admin/#wait-for-service).

<RiakDocsNote>
It is important that you ensure riak_kv is active before restarting the next
node.
</RiakDocsNote>
