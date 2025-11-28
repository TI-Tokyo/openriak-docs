---
title: Buckets and Bucket-types
sidebar_label: "Buckets and Bucket-types"
---

# Buckets

Buckets are essentially a flat namespace in OpenRiak. They allow the same key name to exist in multiple buckets and enable you to apply configurations across keys.

## How Many Buckets Can I Have?

Buckets come with virtually no cost except for when you modify the default bucket properties. Modified bucket properties are gossiped around the cluster and therefore add to the amount of data sent around the network. In other words, buckets using the default bucket type are free. More on that in the next section.

In OpenRiak/Legacy Riak versions 2.0 and later, it is suggested that you use bucket types to namespace and configure all buckets you use. Bucket types have a lower overhead within the cluster than the default bucket namespace but require an additional setup step on the command line.

# Bucket types

## Creating a Bucket Type
When creating a new bucket type, you can create a bucket type without any properties and set individual buckets to be indexed. The step below creates and activates the bucket type:

```bash
riak admin bucket-type create animals '{"props":{}}'
riak admin bucket-type activate animals
```
This will produce the following outputs:

```bash
riak admin bucket-type create animals '{"props":{}}'
animals created

WARNING: After activating animals, nodes in this cluster
can no longer be downgraded to a version of Riak prior to 2.0
ok
```
and

```bash
riak admin bucket-type activate animals
animals has been activated

WARNING: Nodes in this cluster can no longer be
downgraded to a version of Riak prior to 2.0
ok
```

Another possibility is to set the search_index as a default property of the bucket type. This means any bucket under that type will inherit that setting and have its values indexed.

```bash
riak admin bucket-type create animals '{"props":{"search_index":"famous"}}'
riak admin bucket-type activate animals
```