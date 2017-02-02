.. _naming:

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

* Field names should use the `snake_case` style, *not* `CamelCase` or
  `StUdLyCaPs` style.

**TODO** Add patch proposing guidelines for how to name boolean fields.

State vs. Status
----------------

While these two names mean nearly the same thing, there are differences. In
general, 'state' should be used when recording where in a series of steps a
process is in. In other words, 'state' is expected to change, and then only to
a small number of subsequent states. An example of this would be the building
of a VM, which follows a series of steps, and either moves forward to the next
state, or falls into an ERROR state.

Status, on the other hand, should be used for cases where there is no
expectation of a series of changes. A service may have the status of "up" or
"active", and it is expected that it should remain like that unless either and
admin changes it, or a failure occurs.
