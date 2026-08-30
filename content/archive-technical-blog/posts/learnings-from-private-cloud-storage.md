---
title: "Learnings from Private Cloud Storage"
date: "2013-09-26T17:25:15+00:00"
author: "John Burwell"
original_url: "http://basho.com/posts/technical/learnings-from-private-cloud-storage/"
archive_url: "https://web.archive.org/web/20170801115241http://basho.com/posts/technical/learnings-from-private-cloud-storage/"
categories:
  - "Cloud & Deployment"
  - "Use Cases"
---
*September 26, 2013*

Big Data. eCommerce. Mobile. Suddenly, information technology has shifted from cost center to business opportunity. This opportunity favors fast movers with the ability to rapidly execute on emerging trends. Therefore, the length of traditional IT procurement cycles and provisioning processing has become a significant barrier to capitalizing on these opportunities. To increase their operational agility, some organizations are employing public infrastructure as a service (IaaS) or cloud providers (such as Amazon Web Services and Joyent) to rapidly provision compute and storage resources. However, technical incompatibilities, regulatory restrictions, cost at scale, and/or existing capital investments prevent many organizations from utilizing public cloud providers to achieve this operational agility. Private clouds allow these organizations to realize the value of public clouds with the flexibility to comply with their unique combination business and technical requirements.

Fundamentally, a cloud (public or private) creates a composable infrastructure with the following capabilities:

- **Resource Pooling:** Presents compute, storage, and network resources through a unified set of vendor neutral abstractions and manages them based on service-level requirements.
- **Rapid Elasticity:** Optimizes resource allocation based on performance relative to service-level requirements.
- **Self Service:** Delegates management responsibilities for a subset of the infrastructure resources to end-users.
- **Metering/Charge Back:** Records resource utilization on a per customer basis to support usage billing.

Private clouds implement these characteristics by orchestrating infrastructure provisioning and management through the following services:

- **Compute:** Physical or virtual machines with a specified number of processing cores and RAM.
- **Block Storage:** Random access, read/write persistent storage capable of supporting disk partitioning and file systems.
- **Object Storage:** Write-once, read-many (WORM) oriented storage for large files (multiple gigabytes to terabytes in size) accessed through a key-value oriented interface.
- **Network:** Network topology definition and connectivity management between compute, block storage, and object storage services, as well as public networks such as the Internet.

Typically, these services are exposed via an HTTP API, as well as a web-based dashboard allowing end-users to simultaneously script complex workflows and visualize their infrastructure.

Superficially, private clouds appear to be traditional virtualization infrastructures with a web interface and HTTP API. While both models share a number of common components, cloud infrastructures achieve reliability by horizontally scaling commodity hardware instead of vertically scaling specialized hardware. The following table contrasts the storage strategies employed by the traditional virtualization and cloud models:

| **Data Type** | **Traditional Virtualization** | **Cloud** |
| --- | --- | --- |
| Application Data | VM direct attached storage (e.g. NAS, SAN, etc) | Elastic database service (e.g. [Riak](http://basho.com/riak)) |
| Static Content | VM direct attached storage | Object Storage (e.g. [Riak CS](http://basho.com/riak-cloud-storage/)) |
| Templates | VM direct attached storage | Object Storage (e.g. Riak CS) |
| Backups | VM direct attached storage | Object Storage (e.g. Riak CS) |

Static content, templates, and backups typically represent the majority of a system’s storage consumption. Employing object storage to manage this data brings the following benefits to private cloud infrastructures:

- **Reduced Hardware Costs:** By replicating multiple copies of data across a cluster of services, object storage systems such as Riak CS guarantee data durability through software rather than hardware. This approach allows users to employ cheaper commodity hardware using ubiquitous SATA/SAS storage subsystems without sacrificing reliability.
- **Horizontal Scalability:** Since storage coordination and data replication occurs in software, storage is expanded by simply adding new servers to the cluster.
- **Operational Simplicity:** Accessed via HTTP/HTTPS, object storage systems provide secure access to data using a simple, ubiquitous protocol. Unlike iSCSI and Fiber Channel solutions, this approach typically has little to no impact on network infrastructure designs.

The [Apache CloudStack](http://cloudstack.apache.org) IaaS platform has supported Swift-based object storage since version 4.0.0 and S3-based object storage since version 4.1.0. With the 4.2.0, CloudStack supports S3 and Swift as native secondary storage devices – allowing the system to provision and backup VMs directly from an object store. When coupled with Riak CS Enterprise, Apache CloudStack-based clouds are able to replicate template and snapshot data across multi-data centers to meet off-site backup and disaster recovery requirements.

The [OpenStack Object Storage API](http://docs.openstack.org/api/openstack-object-storage/1.0/content/) specifies the semantics of OpenStack’s object storage service. The Swift implementation of this API is provided as the default implementation of this API. With the 1.4.0 release, Riak CS implements both the OpenStack Object Storage API allowing it to serve as a drop-in Swift replacement.

As organizations work to understand the opportunities created by information technology, private clouds have emerged as a key component of their strategies to increase operational agility. While private clouds can be constructed using traditional virtualization approaches, such designs will simply mask core infrastructure brittleness and high infrastructure costs. By embracing design principles such as object storage that underpin cloud infrastructure platforms, organizations can realize the promise of increased operational agility and cost savings.

[John Burwell](https://twitter.com/john_burwell)
