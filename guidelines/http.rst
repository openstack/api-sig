.. _http:

HTTP Guidelines
===============

This document contains guidelines for which HTTP response codes should be used
by OpenStack APIs as well as what HTTP methods should be supported and
preferred.

If something is not covered by this document, projects should follow the
guidelines in RFCs :rfc:`7230`, :rfc:`7231`, :rfc:`7232`, :rfc:`7233`,
:rfc:`7234`, and :rfc:`7235`.

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

* A **500 Internal Server Error** should **not** be returned to the user for
  failures due to user error that can be fixed by changing the request on the
  client side.  500 failures should be returned for any error state that cannot
  be fixed by a client, and requires the operator of the service to perform
  some action to fix. It is also possible that this error can be raised
  deliberately in case of some detected but unrecoverable error such as failure
  to communicate with another service component, eg MessageQueueTimeout,
  IOError caused by a full disk, etc.

HTTP Methods
------------

**TODO**: Provide guidance on what HTTP methods (PUT/POST/PATCH/DELETE, etc)
should always be supported, and which should be preferred.

Conveying error/fault information to the end user
-------------------------------------------------

**TODO**: We should have a section here that describes the recommended way of
transmitting error/fault information back to the user, including any guidelines
on the payload in the response body.
