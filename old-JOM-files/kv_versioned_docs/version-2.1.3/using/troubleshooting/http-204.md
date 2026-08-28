---
title: "HTTP 204"
sidebar_position: 101
sidebar_label: HTTP 204
pagination_label: "HTTP 204"
hide_table_of_contents: true
last_update:
  author: RiakDocs
  date: 2015-12-10
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


In the HTTP standard, a `204 No Content` is returned when the request was successful but there is nothing to return other than HTTP headers.

If you add `returnbody=true` in the `PUT` request, you will receive a `200 OK` and the content you just stored, otherwise you will receive a `204 No Content`.
