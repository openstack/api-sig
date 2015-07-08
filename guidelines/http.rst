.. _http:

HTTP Guidelines
===============

This document contains guidelines for which HTTP response codes should be used
by OpenStack APIs as well as what HTTP methods should be supported and
preferred.

If something is not covered by this document, projects should follow the
guidelines in RFCs `7230 <https://tools.ietf.org/html/rfc7230>`_,
`7231 <https://tools.ietf.org/html/rfc7231>`_,
`7232 <https://tools.ietf.org/html/rfc7232>`_,
`7233 <https://tools.ietf.org/html/rfc7233>`_,
`7234 <https://tools.ietf.org/html/rfc7234>`_, and
`7235 <https://tools.ietf.org/html/rfc7235>`_.

HTTP Response Codes
-------------------

2xx Success Codes
~~~~~~~~~~~~~~~~~

* Synchronous resource creation

 * Response status code must be ``201 Created``
 * Must return a Location header with the URI of the created resource
 * Should return a representation of the resource in the body

* Asynchronous resource creation

  * Response status code must be ``202 Accepted``
  * Must return a Location header set to one of the following:
      * the URI of the resource to be created, if known.
      * the URI of a status resource that the client can use to query the
        progress of the asynchronous operation.

* Synchronous resource deletion

 * Response status code must be ``204 No Content``

* For all other successful calls, the return code should be **200 OK**.

Failure Codes
~~~~~~~~~~~~~

* If the call results in the OpenStack user exceeding his or her quota, the
  return code should be **403 Forbidden**. Do **not** use **413 Request
  Entity Too Large**.

* For badly formatted requests, the return code should be **400 Bad Request**.
  Do **not** use **422 Unprocessable Entity**.

* If a call is made to a known resource URI, but the HTTP method used for the
  request is not supported for that resource, the return code should be **405
  Method Not Allowed**. The response should include the `Allow` header with
  the list of accepted request methods for the resource.

HTTP Methods
------------

**TODO**: Provide guidance on what HTTP methods (PUT/POST/PATCH/DELETE, etc)
should always be supported, and which should be preferred.

* When choosing how to update a stored resource, **PUT** and **PATCH** imply
  different semantics. **PUT** sends a full resource representation (including
  unchanged fields) which will replace the resource stored on the server. In
  contrast, **PATCH** accepts partial representation which will modify the
  server's stored resource. :rfc:`5789` does not specify a partial
  representation format. JSON-patch in :rfc:`6902` specifies a way to send a
  series of changes represented as JSON. One unstandardized alternative is to
  accept missing resource fields as unchanged from the server's saved state of
  the resource. :rfc:`5789` doesn't forbid using PUT in this way, but this
  method makes it possible to lose updates when dealing with lists or sets.

Conveying error/fault information to the end user
-------------------------------------------------

**TODO**: We should have a section here that describes the recommended way of
transmitting error/fault information back to the user, including any guidelines
on the payload in the response body.
