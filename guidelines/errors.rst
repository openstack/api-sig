.. _errors:

Errors
======

Description
-----------

Errors are a crucial part of the developer experience when using an API. As
developers learn the API they inevitably run into errors. The quality and
consistency of the error messages returned to them will play a large part
in how quickly they can learn the API, how they can be more effective with
the API, and how much they enjoy using the API.

This document describes an emerging standard within OpenStack for providing
structured error responses that can be consistently processed and include
coding that will eventually allow errors to be searched for on the web and in
documentation using the value of the ``code`` field. Such codes help to
distinguish the causes of different errors in response to the same HTTP method
and URI, even when the same HTTP status is returned.

.. note:: Services choosing to add these structured error responses are advised
   that doing so is not considered a backwards incompatible change and are
   encouraged to add them without needing to version the service. However,
   when a ``code`` is added to a specific response, subsequent change to that
   code, on that response, is an incompatbile change.

Errors JSON Schema
------------------

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
"SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in :rfc:`2119`.

.. literalinclude:: errors-schema.json
   :language: json

Errors JSON Example
-------------------

.. literalinclude:: errors-example.json
   :language: json

.. note:: This example is completely contrived. This is not how Orchestration
   or Compute responds with errors. It merely illustrates how a service might
   chain together errors. The example hrefs in the ``links`` are examples
   only, but demonstrate that a service should be responsible for publishing
   and maintaining the documentation associated with the error codes the
   service produces.

Errors Documentation
--------------------

The intention of the ``code`` is twofold:

* To provide a convenient and memorable phrase that a human can use when
  communicating with other humans about an error they've experienced, or use
  when searching documentation or their favorite search engine for references
  to the error.

* To act as flow control in client code where the same HTTP status code may be
  used to indicate multiple conditions. A common case is when a
  ``409 Conflict`` may indicate several different ways in which the desired
  state cannot be accommodated and the handling of the conflict should differ.

To satisfy both of these requirements the strings used for the error codes need
to be self-describing and human-readable while also distinct from one another.
Avoiding abbreviation is recommended.

As an example, consider a service that provides a URI, ``/servers/{uuid}``.
There are at least two different ways that a ``404 Not Found`` response may
happen when making a ``GET`` request against that URI. One is that no server
having ``{uuid}`` currently exists. The other is that the URI has been entered
incorrectly (e.g., ``/server/{uuid}``). These conditions should result in
different codes. Two possible codes for these cases are
``compute.server.not_found`` and ``compute.uri.not_found``, respectively.
