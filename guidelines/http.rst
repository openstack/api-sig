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

* For all other successful requests, the return code should be **200 OK**.

* If a request attempts to put a resource into a state which it is
  already in (eg locking an instance which is already locked), the return code
  should be in the **2xx Successful** range (usually matching the return code
  which would be given if the state had changed). It is not appropriate to use
  **409 Conflict** when the resulting state of the resource is as the user
  requested.

Failure Codes
~~~~~~~~~~~~~

* If the request results in the OpenStack user exceeding his or her quota, the
  return code should be **403 Forbidden**. Do **not** use **413 Request
  Entity Too Large**.

* For badly formatted requests, the return code should be **400 Bad Request**.
  Do **not** use **422 Unprocessable Entity**.

* If a request is made to a known resource URI, but the HTTP method used for
  the request is not supported for that resource, the return code should be
  **405 Method Not Allowed**. The response should include the `Allow` header
  with the list of accepted request methods for the resource.

* If a request is made which attempts to perform an action on a resource which
  is already performing that action and therefore the request cannot be
  fulfilled (eg snapshotting an instance which is already in the process of
  snapshotting), the return code should be **409 Conflict**.

* A **500 Internal Server Error** should **not** be returned to the user for
  failures due to user error that can be fixed by changing the request on the
  client side.  500 failures should be returned for any error state that cannot
  be fixed by a client, and requires the operator of the service to perform
  some action to fix.

HTTP Methods
------------

**TODO**: Provide guidance on what HTTP methods (PUT/POST/PATCH/DELETE, etc)
should always be supported, and which should be preferred.

Conveying error/fault information to the end user
-------------------------------------------------

**TODO**: We should have a section here that describes the recommended way of
transmitting error/fault information back to the user, including any guidelines
on the payload in the response body.
