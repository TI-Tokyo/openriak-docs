---
title: Buckets and Bucket-types
sidebar_label: "Buckets and Bucket-types"
date: 2026-07-03
---
[root site]: [!site]
[root project]: [!project]
[root version]: [!version]
[buckets]: #buckets
[howmany]: #how-many-buckets-can-i-have
[buckettypes]: #bucket-types
[howwork]: #how-do-bucket-types-work
[when]: #when-to-use-bucket-types
[createactivate]: #creating-and-activating-a-bucket-type
[namespace]: #bucke-types-as-namespaces
[allowmulti]: #bucket-types-and-the-allow_mult-setting

>[!MEMO] Buckets
>Buckets are essentially a flat namespace in OpenRiak. They allow the same key name to exist in multiple buckets and enable you to apply configurations across keys.

## How many Buckets can I have?

Buckets come with virtually no cost except for when you modify the default bucket properties. Modified bucket properties are gossiped around the cluster and therefore add to the amount of data sent around the network. In other words, buckets using the default bucket type are free. More on that in the next section.

In OpenRiak/Legacy Riak versions 2.0 and later, it is suggested that you use bucket types to namespace and configure all buckets you use. Bucket types have a lower overhead within the cluster than the default bucket namespace but require an additional setup step on the command line.

# Bucket types

Bucket types allow you to have groups of buckets that share configuration details and for OpenRiak users to manage bucket properties more efficiently than in the older configuration system based on bucket properties.

## How do Bucket Types work

    * Bucket Types allow you to create a set of bucket configurations and apply those configurations to  multiple buckets at the same time, rather than configured on a per-bucket basis that the older bucket properties system used.

    * All bucket properties can be udpated using Bucket Types except for the [datatype](#bucket-types) and the `consistent` properties.

    * Bucket types deliver better performance than bucket properties because their configuration is defined once and gossiped once, avoiding the need to propagate divergent settings for every individual bucket. This reduces cluster‑wide gossip and lowers computational overhead.

It is important to note that buckets are not assigned types in the same way that they are configured when using bucket properties. You cannot simply take a bucket `my_bucket` and assign it a type the way that you would, say, set `allow_mult` to `false` or `n_val` to `5`, because there is no `type` parameter contained within the bucket’s properties (i.e. `props`).

Instead, bucket types are applied to buckets on the basis of how those buckets are queried. Queries involving bucket types take the following form:

    ```bash
        GET/PUT/DELETE /types/<type>/buckets/<bucket>/keys/<key>
    ```

In older, bucket property-based systems, only the bucket and key are specified in queries:

    ```bash
        GET/PUT/DELETE /buckets/<bucket>/keys/<key>
    ```

# When to use Bucket types

Bucket Types should always be used in OpenRiak and Legacy Riak Versions from 2.0 onwards for the following reasosn:

    * Bucket types are more flexible because they enable you to define a bucket configuration and then change it if you need to.

    * Bucket types are more reliable because the buckets that bear a given type only have their properties changed when the type is changed. Previously, it was possible to change the properties of a bucket only through client requests.

    * Whereas bucket properties can only be altered by clients interacting with Riak, bucket types are more of an operational concept. The `riak admin bucket-type` interface (discussed in depth below) enables you to manage bucket configurations on the operations side, without recourse to Riak clients.

## Creating and Activating a Bucket Type

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

## Bucke types as namespaces 

From Legacy Riak 2.0, Bucket types can be used as an additional namespace on top of buckets and keys.

This allows the same bucket name to be associated with completely different data if used with a different bucket type. This allows two requests to be made with the same bucket and key names but different types, reaching different objects such as the example below:

    ```bash
        curl http://localhost:8098/types/type1/buckets/my_bucket/keys/my_key
        curl http://localhost:8098/types/type2/buckets/my_bucket/keys/my_key
    ```

>[!NOTE]Note on Object Location
>From Legacy Riak 2.0.x onwards, all requests must be made to a location specified by a bucket type, bucket, and key rather than to a bucket/key pair, as in previous versions.

## Default Bucket Properties

Below is a listing of the default bucket properties (i.e. props) associated with the default bucket type:

    ```JSON
        {
        "props": {
            "allow_mult": false,
            "basic_quorum": false,
            "big_vclock": 50,
            "chash_keyfun": {
              "fun": "chash_std_keyfun",
              "mod": "riak_core_util"
         },
            "dvv_enabled": false,
            "dw": "quorum",
            "last_write_wins": false,
            "linkfun": {
              "fun": "mapreduce_linkfun",
              "mod": "riak_kv_wm_link_walker"
            },
            "n_val": 3,
            "notfound_ok": true,
            "old_vclock": 86400,
            "postcommit": [],
            "pr": 0,
            "precommit": [],
            "pw": 0,
            "r": "quorum",
            "rw": "quorum",
            "small_vclock": 50,
            "w": "quorum",
            "young_vclock": 20
        }
    }
    ```

## Bucket Types and the `allow_mult` setting

Prior to Legacy Riak 2.0, Legacy Riak created siblings in the case of conflicting updates only when explicitly instructed to do so, i.e. when `allow_mult` is to `true`. The default `allow_mult` setting was `false`.

In versions of Legacy Riak from 2.0 onwards, and all versions of OpenRiak, this has changed. There are now two different default settings for `allow_multi`.

1. For the `default` bucket type, the `allow_mult` value is set to `false` by default. 
2. For all newly created bucket types, `allow_mult` is set to `true` by default. You can set this to `false` if you do not want to resolve sibling conflicts, but you need to do this explicitly.

This allows applications that ignored conflict resolutions in certain buckets (or all buckets) in the past, can continue to do this. While new applications should retain and resolve siblings with their own logic.


The following example shows you the `allow_mult` propery on a default bucket, vs a newly created one:

    ```bash
        riak admin bucket-type status default | grep allow_mult
    ```

This produces the following output:

    ```bash
        allow_mult: false
    ```

Next, we're going to create a new bucket type called `n_val_of_2` which will set the `n_val` to 2, but does not set `allow_mult`:

    ```bash
        riak admin bucket-type create n_val_of_2 '{"props":{"n_val":2}}'
    ```

This will produce the following output:

    ```bash
        n_val_of_2 created
        ok
    ```

When we specified the bucket type's properties above, we did not explicitly change the `allow_mult` value. But, if we now view the bucket type's properties, we can see that the value of `allow_mult` is set to `true`:

    ```bash
        riak admin bucket-type status n_val_of_2 | grep allow_mult
    ```

Producing the following output:

    ```bash
        allow_mult: true
    ```
   
## Bucket Type Example

Let’s say that you’d like to create a bucket type called `user_account_bucket` with a pre-commit hook called `syntax_check` and two post-commit hooks called `welcome_email` and `update_registry`. This would involve four steps:

    1. Creating a JavaScript object containing the appropriate `props` settings:

    ```json
        {
         "props": {
         "precommit": ["syntax_check"],
         "postcommit": ["welcome_email", "update_registry"]
         }
        }
    ```

    2. Passing that JSON to the `bucket-type create` command:

    ```bash
        riak admin bucket-type create user_account_bucket '{"props":{"precommit": ["syntax_check"], ... }}'
    ```

    3. Verifying that the type is ready to be activated.
    Once the type is created, you can check whether your new type is ready to be activated by running:

    ```bash
        riak admin bucket-type status user_account_bucket
    ```

    If the first line reads `user_account_bucket` has been created and may be activated, then you can proceed to the next step. If it reads `user_account_bucket` has been created and is not ready to activate, then wait a moment and try again. If it still does not work, then there may be network partition or other issues that need to be addressed in your cluster.

    4. Activating the new bucket type:

    ```bash
        riak admin bucket-type activate user_account_bucket
    ```

    If activation is successful, the console will return `user_account_bucket has been activated`. The bucket type is now ready to be used.

