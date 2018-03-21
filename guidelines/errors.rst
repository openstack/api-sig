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
   chain together errors.

Errors Documentation
--------------------

TODO(sdague): Expand on the vision behind Errors Documentation
