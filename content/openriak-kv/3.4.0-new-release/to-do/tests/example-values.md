---
title: Personalized example values
description: Demonstration of browser-local example values.
draft: true
---

Set example values using the gear icon in the site header.

Cluster: {{< example "cluster" 1 >}}. Second cluster: {{< example "cluster" 2 >}}.

Inline node: `{{< example "node" 1 >}}`.

```bash
printf '%s\n' '{{< example "cluster" 1 >}}'
curl http://{{< example "listener" 1 "host" >}}:{{< example "listener" 1 "port" >}}/ping
```

Cluster size: {{< example "clusterSize" >}}. Ring size: {{< example "ringSize" >}}.

These example values do not change the defaults in the configuration reference.
