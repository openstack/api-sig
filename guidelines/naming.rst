Naming Conventions
==================

This topic document serves to provide guidance on how to name resources in
OpenStack public REST APIs so that our APIs feel consistent and professional.

REST API resource names
-----------------------

* A resource in a REST API is always represented as the plural of an entity
  that is exposed by the API.

* Resource names exposed in a REST API should use all lowercase characters.

* Resource names *may* include hyphens.

* Resource names should *not* include underscores or other punctuation
  (sole exception is the hyphen).

Fields in an API request or response body
-----------------------------------------

HTTP requests against an API may contain a body which is typically a serialized
representation of the resource that the user wished to create or modify.
Similarly, HTTP responses contain a body that is usually the serialized
representation of a resource that was created, modified, or listed by the
server.

Fields within these serialized request and response bodies should be named
according to these guidelines:

* Field names should use `snake_case` style, *not* `CamelCase` or `MixedCase`
  style.

**TODO** Add patch proposing guidelines for how to name boolean fields.

**TODO** Add patch proposing guidelines for naming state/status fields.
