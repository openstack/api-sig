HTTP Response Codes
===================

This document contains guidelines for which HTTP response codes should be used
by OpenStack APIs.

If something is not covered by this document, projects should follow the
guidelines in [RFC 2616](rfc2616).

Success Codes
-------------

* If the API call creates a resource on a server, the return code should be
  **201 Created**.

* If the API call succeeds, but the result of the call has created an
  asynchronous task that will need to be polled to get completion or state
  information, the return code should be **202 Accepted**, and the body of the
  request should contain a link that the client can follow in order to get such
  state information.

* For all other successful calls, the return code should be **200 OK**.

Failure Codes
-------------

* If the call results in the OpenStack user exceeding his or her quota, the
  return code should be **403 Forbidden**. Do ***not*** use **413 Request
  Entity Too Large**.

* For badly formatted requests, the return code should be **400 Bad Request**.
  Do ***not*** use **422 Unprocessable Entity**.

TODO
----

We should have a section here that describes the recommended way of
transmitting error/fault information back to the user, including any guidelines
on the payload in the response body.

[rfc2616]: https://tools.ietf.org/html/rfc2616
