.. _http:

HTTP Guidelines
===============

This document contains guidelines for which HTTP response codes should be used
by OpenStack APIs as well as what HTTP methods should be supported and
preferred.

If something is not covered by this document, projects should follow the
guidelines in [RFC 2616](https://tools.ietf.org/html/rfc2616).

HTTP Response Codes
-------------------

Success Codes
~~~~~~~~~~~~~

* If the API call creates a resource on a server, the return code should be
  **201 Created**.

* Asynchronous resource creation

  * Response status code must be ``202 Accepted``
  * Must return a Location header set to one of the following:
      * the URI of the resource to be created, if known.
      * the URI of a status resource that the client can use to query the
        progress of the asynchronous operation.

* For all other successful calls, the return code should be **200 OK**.

Failure Codes
~~~~~~~~~~~~~

* If the call results in the OpenStack user exceeding his or her quota, the
  return code should be **403 Forbidden**. Do **not** use **413 Request
  Entity Too Large**.

* For badly formatted requests, the return code should be **400 Bad Request**.
  Do **not** use **422 Unprocessable Entity**.

HTTP Methods
------------

**TODO**: Provide guidance on what HTTP methods (PUT/POST/PATCH/DELETE, etc)
should always be supported, and which should be preferred.

Conveying error/fault information to the end user
-------------------------------------------------

**TODO**: We should have a section here that describes the recommended way of
transmitting error/fault information back to the user, including any guidelines
on the payload in the response body.
