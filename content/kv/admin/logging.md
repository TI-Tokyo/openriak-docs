---
title: Logging
sidebar_label: "Logging"
---

Buckets are essentially a flat namespace in Riak. They allow the same key name to exist in multiple buckets and enable you to apply configurations across keys.

How Many Buckets Can I Have?
Buckets come with virtually no cost except for when you modify the default bucket properties. Modified bucket properties are gossiped around the cluster and therefore add to the amount of data sent around the network. In other words, buckets using the default bucket type are free. More on that in the next section.

Creating a Bucket Type
When creating a new bucket type, you can create a bucket type without any properties and set individual buckets to be indexed. The step below creates and activates the bucket type:

Shell
riak admin bucket-type create animals '{"props":{}}'
riak admin bucket-type activate animals
And this step applies the index to the cats bucket, which bears the animals bucket type we just created and activated:

CURL
curl -XPUT $RIAK_HOST/types/animals/buckets/cats/props \
     -H 'Content-Type: application/json' \
     -d '{"props":{"search_index":"famous"}}'
Another possibility is to set the search_index as a default property of the bucket type. This means any bucket under that type will inherit that setting and have its values indexed.

Shell
riak admin bucket-type create animals '{"props":{"search_index":"famous"}}'
riak admin bucket-type activate animals