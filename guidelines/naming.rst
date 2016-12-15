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

* Field names should use `snake_case` style, *not* `CamelCase` or `MixedCase`
  style.

Boolean fields
--------------

Boolean fields should be named so that the name completes the phrase "This is
_____" or "This has ____". For example, if you need a field to indicate whether
the item in question is enabled, then "enabled" would be the proper form, as
opposed to something like "is_enabled". Similarly, to indicate a network that
uses DHCP, the field name "dhcp_enabled" should be used, rather than forms such
as "enable_dhcp" or just "dhcp".

It is also strongly recommended that negative naming be avoided, so use
'enabled' instead of 'disabled' or 'not_enabled'. The reason for this is that
it is difficult to understand double negatives when reading code. In this case,
"not_enabled = False" is harder to understand than "enabled = True".

Boolean parameters
------------------

There are two types of boolean parameters: those that are used to supply the
value for a boolean field as described above, and those that are used to
influence the behavior of the called method. In the first case, the name of the
parameter should match the name of the field. For example, if you are supplying
data to populate a field named 'enabled', the parameter name should also be
'enabled'. In the second case, though, where the parameter is used to toggle
the behavior of the called method, the name should be more verb-like. A example
of this form is the parameter "force", which is commonly used to indicate that
the method should carry out its action without the normal safety checks. And as
with boolean fields, the use of negative naming for boolean parameters is
strongly discouraged, for the same reasons.

**TODO** Add patch proposing guidelines for naming state/status fields.
