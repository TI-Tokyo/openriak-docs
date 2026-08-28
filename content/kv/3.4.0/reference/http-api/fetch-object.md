---
title: 'Fetch an object with the HTTP API'
description: 'Document the complete HTTP contract for this operation, including parameters, representations, examples, and errors.'
weight: 4
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'developers'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\http\fetch-object.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/ObjectAPI.html#accessing-legacy-objects'
  - 'https://openriak.github.io/riak/ObjectAPI.html#http-api-definition---fetch'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Document the complete HTTP contract for this operation, including parameters, representations, examples, and errors.

## Details

### HTTP Fetch Object

Reads an object from the specified bucket/key.

#### Request

```bash
GET /types/type/buckets/bucket/keys/key
GET /buckets/bucket/keys/key
```

Important headers:

* `Accept` - When `multipart/mixed` is the preferred content-type, objects with
siblings will return all siblings in single request. See [Siblings examples](#siblings-examples). See
also RFC 2616 - [Accept header definition](http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.1).

Optional headers:

* `If-None-Match` and `If-Modified-Since` invoke conditional request semantics,
matching on the `ETag` and `Last-Modified` of the object, respectively.  If the
object fails one of the tests (that is, if the ETag is equal or the object is
unmodified since the supplied timestamp), Riak will return a `304 Not Modified`
response. See also RFC 2616 - [304 Not Modified](http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3.5).

Optional query parameters:

* `r` - (read quorum) how many replicas need to agree when retrieving the
object ([default is defined by the bucket](/kv/3.4.0/reference/http-api/set-bucket-properties/))
* `pr` - how many primary replicas need to be online when doing the read
([default is defined by the bucket](/kv/3.4.0/reference/http-api/set-bucket-properties/))
* `basic_quorum` - whether to return early in some failure cases (eg. when r=1
and you get 2 errors and a success `basic_quorum=true` would return an error)
([default is defined by the bucket](/kv/3.4.0/reference/http-api/set-bucket-properties/))
* `notfound_ok` - whether to treat notfounds as successful reads for the
purposes of R ([default is defined by the bucket](/kv/3.4.0/reference/http-api/set-bucket-properties/))
* `vtag` - when accessing an object with siblings, which sibling to retrieve.
Scroll down to the [Manually requesting siblings](#manually-requesting-siblings) example for more information.

#### Response

Normal response codes:

* `200 OK`
* `300 Multiple Choices`
* `304 Not Modified` (when using conditional request semantics)

Typical error codes:

* `400 Bad Request` - e.g. when r parameter is invalid (> N)
* `404 Not Found` - the object could not be found on enough partitions
* `503 Service Unavailable` - the request timed out internally

Important headers:

* `Content-Type` - the media type/format
* `X-Riak-Vclock` - the opaque vector clock for the object
* `X-Riak-Meta-*` - any user-defined metadata defined when storing the object
* `ETag` - the entity tag for the object, useful for conditional GET operations
and validation-based caching
* `Last-Modified` - a timestamp for when the object was last written, in HTTP
datetime format
* `Link` - user- and system-defined links to other resources. [Read more about Links.](/kv/3.4.0/explanation/foundations/glossary/)

The body of the response will be the contents of the object except when siblings
are present.

**Siblings**
When `allow_mult` is set to true in the bucket properties, concurrent updates
are allowed to create "sibling" objects, meaning that the object has any
number of different values that are related to one another by the vector
clock.  This allows your application to use its own conflict resolution
technique.

An object with multiple sibling values will result in a `300 Multiple Choices`
response.  If the `Accept` header prefers `multipart/mixed`, all siblings will
be returned in a single request as sections of the `multipart/mixed` response
body.  Otherwise, a list of "vtags" will be given in a simple text format. You
can request individual siblings by adding the `vtag` query parameter. Scroll
down to the 'manually requesting siblings' example below for more information.

To resolve the conflict, store the resolved version with the `X-Riak-Vclock`
given in the response.

#### Simple Example

```curl
$ curl -v http://127.0.0.1:8098/buckets/test/keys/doc2
* About to connect() to 127.0.0.1 port 8098 (#0)
*   Trying 127.0.0.1... connected
* Connected to 127.0.0.1 (127.0.0.1) port 8098 (#0)
> GET /buckets/test/keys/doc2 HTTP/1.1
> User-Agent: curl/7.19.4 (universal-apple-darwin10.0) libcurl/7.19.4 OpenSSL/0.9.8l zlib/1.2.3
> Host: 127.0.0.1:8098
> Accept: */*
>
< HTTP/1.1 200 OK
< X-Riak-Vclock: a85hYGBgzGDKBVIsbLvm1WYwJTLmsTLcjeE5ypcFAA==
< Vary: Accept-Encoding
< Server: MochiWeb/1.1 WebMachine/1.9.0 (participate in the frantic)
< Link: </buckets/test>; rel="up"
< Last-Modified: Wed, 10 Mar 2010 18:11:41 GMT
< ETag: 6dQBm9oYA1mxRSH0e96l5W
< Date: Fri, 30 Sep 2011 15:24:35 GMT
< Content-Type: application/json
< Content-Length: 13
<
* Connection #0 to host 127.0.0.1 left intact
* Closing connection #0
{"foo":"bar"}
```

#### Siblings examples

##### Manually requesting siblings

Simple call to fetch an object that has siblings:

```curl
$ curl -v http://127.0.0.1:8098/buckets/test/keys/doc
* About to connect() to 127.0.0.1 port 8098 (#0)
*   Trying 127.0.0.1... connected
* Connected to 127.0.0.1 (127.0.0.1) port 8098 (#0)
> GET /buckets/test/keys/doc HTTP/1.1
> User-Agent: curl/7.19.4 (universal-apple-darwin10.0) libcurl/7.19.4 OpenSSL/0.9.8l zlib/1.2.3
> Host: 127.0.0.1:8098
> Accept: */*
>
< HTTP/1.1 300 Multiple Choices
< X-Riak-Vclock: a85hYGDgyGDKBVIszMk55zKYEhnzWBlKIniO8kGF2TyvHYIKf0cIszUnMTBzHYVKbIhEUl+VK4spDFTPxhHzFyqhEoVQz7wkSAGLMGuz6FSocFIUijE3pt5HlsgCAA==
< Vary: Accept, Accept-Encoding
< Server: MochiWeb/1.1 WebMachine/1.9.0 (participate in the frantic)
< Date: Fri, 30 Sep 2011 15:24:35 GMT
< Content-Type: text/plain
< Content-Length: 102
<
Siblings:
16vic4eU9ny46o4KPiDz1f
4v5xOg4bVwUYZdMkqf0d6I
6nr5tDTmhxnwuAFJDd2s6G
6zRSZFUJlHXZ15o9CG0BYl
* Connection #0 to host 127.0.0.1 left intact
* Closing connection #0
```

Now request one of the siblings directly:

```curl
$ curl -v http://127.0.0.1:8098/buckets/test/keys/doc?vtag=16vic4eU9ny46o4KPiDz1f
* About to connect() to 127.0.0.1 port 8098 (#0)
*   Trying 127.0.0.1... connected
* Connected to 127.0.0.1 (127.0.0.1) port 8098 (#0)
> GET /buckets/test/keys/doc?vtag=16vic4eU9ny46o4KPiDz1f HTTP/1.1
> User-Agent: curl/7.19.4 (universal-apple-darwin10.0) libcurl/7.19.4 OpenSSL/0.9.8l zlib/1.2.3
> Host: 127.0.0.1:8098
> Accept: */*
>
< HTTP/1.1 200 OK
< X-Riak-Vclock: a85hYGDgyGDKBVIszMk55zKYEhnzWBlKIniO8kGF2TyvHYIKf0cIszUnMTBzHYVKbIhEUl+VK4spDFTPxhHzFyqhEoVQz7wkSAGLMGuz6FSocFIUijE3pt5HlsgCAA==
< Vary: Accept-Encoding
< Server: MochiWeb/1.1 WebMachine/1.9.0 (participate in the frantic)
< Link: </buckets/test>; rel="up"
< Last-Modified: Wed, 10 Mar 2010 18:01:06 GMT
< ETag: 16vic4eU9ny46o4KPiDz1f
< Date: Fri, 30 Sep 2011 15:24:35 GMT
< Content-Type: application/x-www-form-urlencoded
< Content-Length: 13
<
* Connection #0 to host 127.0.0.1 left intact
* Closing connection #0
{"bar":"baz"}
```

##### Get all siblings in one request

```curl
$ curl -v http://127.0.0.1:8098/buckets/test/keys/doc -H "Accept: multipart/mixed"
* About to connect() to 127.0.0.1 port 8098 (#0)
*   Trying 127.0.0.1... connected
* Connected to 127.0.0.1 (127.0.0.1) port 8098 (#0)
> GET /buckets/test/keys/doc HTTP/1.1
> User-Agent: curl/7.19.4 (universal-apple-darwin10.0) libcurl/7.19.4 OpenSSL/0.9.8l zlib/1.2.3
> Host: 127.0.0.1:8098
> Accept: multipart/mixed
>
< HTTP/1.1 300 Multiple Choices
< X-Riak-Vclock: a85hYGDgyGDKBVIszMk55zKYEhnzWBlKIniO8kGF2TyvHYIKf0cIszUnMTBzHYVKbIhEUl+VK4spDFTPxhHzFyqhEoVQz7wkSAGLMGuz6FSocFIUijE3pt5HlsgCAA==
< Vary: Accept, Accept-Encoding
< Server: MochiWeb/1.1 WebMachine/1.9.0 (participate in the frantic)
< Date: Fri, 30 Sep 2011 15:24:35 GMT
< Content-Type: multipart/mixed; boundary=YinLMzyUR9feB17okMytgKsylvh
< Content-Length: 766
<

--YinLMzyUR9feB17okMytgKsylvh
Content-Type: application/x-www-form-urlencoded
Link: </buckets/test>; rel="up"
Etag: 16vic4eU9ny46o4KPiDz1f
Last-Modified: Wed, 10 Mar 2010 18:01:06 GMT

{"bar":"baz"}
--YinLMzyUR9feB17okMytgKsylvh
Content-Type: application/json
Link: </buckets/test>; rel="up"
Etag: 4v5xOg4bVwUYZdMkqf0d6I
Last-Modified: Wed, 10 Mar 2010 18:00:04 GMT

{"bar":"baz"}
--YinLMzyUR9feB17okMytgKsylvh
Content-Type: application/json
Link: </buckets/test>; rel="up"
Etag: 6nr5tDTmhxnwuAFJDd2s6G
Last-Modified: Wed, 10 Mar 2010 17:58:08 GMT

{"bar":"baz"}
--YinLMzyUR9feB17okMytgKsylvh
Content-Type: application/json
Link: </buckets/test>; rel="up"
Etag: 6zRSZFUJlHXZ15o9CG0BYl
Last-Modified: Wed, 10 Mar 2010 17:55:03 GMT

{"foo":"bar"}
--YinLMzyUR9feB17okMytgKsylvh--
* Connection #0 to host 127.0.0.1 left intact
* Closing connection #0
```

#### HTTP API Definition - Fetch

Fetch requests for objects should be sent using the `GET` method, or the HEAD method.

When using the HEAD method the request will still result in the object value being read by Riak, but the value will be stripped before returning the object - the process is not currently optimised. A HEAD response may not contain a valid content-length.

Supported HTTP request headers for GET:

- `authorization`; optional, for tls-protected requests only when [Riak security is enabled](/kv/3.4.0/how-to/secure/).
- `accept: multipart/mixed`; optional, will cause results in a conflicted state to return all siblings as one multipart-mime object body.  Without this option a list of sibling vtags will be returned, and each `vtag` may be fetched using the `vtag=<vtag>` query parameter in the URL.

Expected HTTP response headers for GET:

- `x-riak-vclock`; an encoded representation of the version_vector, must be provided in any subsequent update message to indicate which version of the object is to be updated.
- `x-riak-meta-<key>: <value>`; potentially multiple headers representing the user metadata for the object.
- `x-riak-index-<field> : <value1>, <value2>`; potentially multiple headers representing the current index values for the object.
- `content-type: <content_type>`; the content-type provided when the object was stored.

#### Accessing Legacy Objects

As well as typed buckets, Riak offers support for untyped buckets for backwards compatibility.  Using the HTTP API for such buckets is the same as using typed buckets, except that the URI for keys in untyped buckets is `buckets/Bucket/keys/Key` (i.e. as before but without the prefix of `types\TypedBucket`).
