---
title: "Yokozuna Pre-release 0.2.0 Now Available"
date: "2012-12-31T00:00:00+00:00"
author: "Basho"
original_url: "http://basho.com/posts/technical/yokozuna-pre-release-0-2-0-now-available/"
archive_url: "https://web.archive.org/web/20170801115617http://basho.com/posts/technical/yokozuna-pre-release-0-2-0-now-available/"
categories:
  - "Releases"
  - "Search & Analytics"
---
*December 31, 2012*

Happy Holidays from all of us here at Basho. We’ve got some new code to help you ring in the new year. [Ryan Zezeski](https://twitter.com/rzezeski) and others have been hard at work on [Yokozuna](https://github.com/rzezeski/yokozuna), the next generation of Riak Search that marries Riak with Apache Solr.

The latest pre-release, 0.2.0, was just tagged, and there’s plenty to be excited about for those of you who are interested in test-driving the code. In addition to various bug fixes, some of the new features include:

- [Active Anti Entropy Support](https://github.com/rzezeski/yokozuna/commit/7a32c6fce7b3d30de0f5f3f0d7a9a6ac29460f9f) – Automatic background processing that seeks out and rectifies divergences between data stored in Riak and indexes stored in Yokozuna.
- [Benchmark Scripts](https://github.com/rzezeski/yokozuna/tree/master/misc/bench) – A pre-built collection of benchmarking scripts for automating performance testing.
- Sibling Support – When enabled, Yokozuna will now index all object versions. It will also handle index cleanup upon sibling resolution.

The full release notes [are up on the GitHub repo](https://github.com/rzezeski/yokozuna/blob/master/docs/RELEASE_NOTES.md#020).

## Contributors

Commits in this release came from Ryan Zezeski, Eric Redmond, and Dan Reverri. Mark Steele also reported a few issues that were fixed in this release.

## Use Yokozuna

**Remember that this is alpha software, and won’t be officially supported by Basho until a future release**. That said, Ryan and the team are actively looking for beta testers with use cases that might be appropriate for Yokozuna. If you’re in the market for scalable, distributed full-text search, [join the Riak Mailing List](http://lists.basho.com/mailman/listinfo/riak-users_lists.basho.com) and start asking questions.

There’s a pre-built [Yokozuna AWS AMI](https://github.com/rzezeski/yokozuna/blob/master/docs/EC2.md) (ami-8b8d03e2) with the latest changes that’ll make it easy to take Yokozuna for a test drive.

And if you’re looking for a high-level introduction to Yokozuna, take 30 minutes to [watch Ryan’s RICON2012 talk](https://vimeo.com/54266574) or browse the [matching slide deck](https://speakerdeck.com/basho/yokozuna-ricon).

Enjoy.

[The Basho Team](https://twitter.com/basho)
