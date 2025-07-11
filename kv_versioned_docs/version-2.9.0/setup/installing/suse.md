---
title: "SUSE"
sidebar_position: 307
sidebar_label: SUSE
pagination_label: "SUSE"
hide_table_of_contents: true
last_update:
  author: RiakDocs
  date: 2019-11-21
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


[install verify]: ./../verify

<RiakDocsNote title="SUSE End of Life (EOL) for Riak KV 2.2.3">
SUSE is no longer supported in Riak KV 2.9.0+. If you are interested in using Riak KV on SUSE, you can still [build from source](../source). The steps below have been left here for reference only and are no longer maintained.
</RiakDocsNote>

Riak KV can be installed on OpenSuse and SLES systems using a binary package. The following steps have been tested to work with Riak on
the following x86/x86_64 flavors of SuSE:

* SLES11-SP1
* SLES11-SP2
* SLES11-SP3
* SLES11-SP4
* OpenSUSE 11.2
* OpenSUSE 11.3
* OpenSUSE 11.4

## Installing with rpm

```bash
wget https://files.tiot.jp/riak/kv/2.2/2.2.3/sles/11/riak-2.2.3-1.SLES11.x86_64.rpm
sudo rpm -Uvh riak-2.2.3-1.SLES11.x86_64.rpm
```

## Next Steps

Now that Riak is installed, check out [Verifying a Riak Installation][install verify].
