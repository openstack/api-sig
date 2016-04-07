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
