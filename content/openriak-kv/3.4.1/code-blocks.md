---
title: 'Code Block test'
description: 'Test how code blocks get displayed.'
weight: 998
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'test-page'
draft: true
audience:
  - 'operators'
  - 'developers'
source_material:
  - 'generated-configuration-metadata'
tags: ['kv', 'reference', 'codeblock', 'test']
editorial_review: 'not-required'
technical_review: 'required'
last_reviewed: '2026-09-02'
review_scope: 'shortcode-integration'
---

Use this draft page to test how code blocks are rendered.

## Filename for downloads

Fullname

```text {filename="this-is-a-fullname"}
This is a fullname
```

Partial name

```text {partialname="this-is-a-partialname"}
This is a partial name
```

Fullname with extension

```text {filename="this-is-a-fullname", extension="textfile"}
This is a fullname with extension
```

Partial name with extension

```text {partialname="this-is-a-partialname", extension="textfile"}
This is a partial name with extension
```

Just with extension

```text {extension="textfile"}
This is just with extension
```

## Bash command wrap

No options

```bash
command subcommand subsubcommand
```

Really long with no options

```bash
command subcommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand
```

Really long with a quoted string:

```bash
command subcommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand "quoted string content quoted string content quoted string content quoted string content quoted string content quoted string content quoted string content quoted string content quoted string content quoted string content quoted string content quoted string content quoted string content quoted string content quoted string content quoted string content quoted string content quoted string content quoted string content quoted string content quoted string content quoted string content quoted string content" anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand anothercommand
```

Single Option

```bash
command -option
```

Single Option with value

```bash
command -option "bob"
```

Multiple Options

```bash
command -option "bob" -f -terry alpha -path /var/log/riak/error.log
```

Multiple options with short quoted value

```bash
command -option "bob" -f -terry alpha -path "quoted string content" -otherOption
```

Multiple options with long quoted value

```bash
command -option "bob" -f -terry alpha -path "quoted string content quoted string content quoted string content quoted string content quoted string content quoted string content quoted string content quoted string content quoted string content quoted string content quoted string content quoted string content quoted string content quoted string content quoted string content" -otherOption
```

## Language tests

Text

```text {filename="riak.conf"}
storage_backend = bitcask
```

Conf

```conf {filename="riak"}
ring_size = 64
```

Erlang

```erlang {partialname="ring-size"}
application:set_env(riak_core, ring_creation_size, 64).
```

Advanced Config

```advancedconfig {partialname="advanced-ring-size"}
[{riak_core, [{ring_creation_size, 64}]}].
```

Bash

```bash {partialname="start-riak"}
# Blank lines must survive Split command and download.

riak start --config /etc/riak/riak.conf --name riak@127.0.0.1 --set-cookie openriak-cluster

riak ping --node riak@127.0.0.1
```

YAML

```yaml {partialname="listener-example" extension="yml"}
listener.http.internal = 127.0.0.1:8098
```
