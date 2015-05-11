.. _http:

HTTP Guidelines
===============

The HTTP RFC is a quite large specification. The HTTP 1.1
specification :rfc:`2616` clocks in at 175 pages. Published in
1999 it assumes a certain use of the HTTP protocol in the web browser
/ server framework. The idea for the use of HTTP as a more generic API
layer only emerged a year after the publication of HTTP 1.1 in
`Chapter 5 of Roy Fieldings PhD thesis
<https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm>`_
and was not widely adopted until many years later.

It's important to realize that concepts and constructs that we want to
manipulate in any given system will not be a perfect match with the
concepts and constraints of HTTP. These mismatches can indicate a
clearly wrong usage of HTTP, a special case to meet requirements, or
an opportunity to improve an existing design. Any recommendation about
using HTTP should come with substantial explanation about why that's
the best approach that we can determine at the time. This provides the
justification for the decision in the present, and bread crumbs in the
future if that justification no longer holds.

HTTP defines a set of standard headers, content negotiation with mime
types, well defined status codes, a url structure, and methods on such
urls.

If something is not covered by this document, or seems ambiguous after
looking at these guidelines, implementers are encouraged to start a
mailing list thread (with references to what they believe are relevant
RFC sections) to clarify and to help make these guidelines more clear
in the future. However, like legal code, an RFC is only a starting
point. Precedents and common usage shape what an active standard
really means.

*Note:* in recent years :rfc:`2616` was split into a multipart
document in :rfc:`7230`, :rfc:`7231`, :rfc:`7232`, :rfc:`7233`,
:rfc:`7234`, and :rfc:`7235`.  No major functional changes are in
these documents, but they are just reorganized for readability, and
small clarifying corrections were made.

HTTP Response Codes
-------------------

HTTP defines a set of standard response codes on requests, they are
largely grouped as follows:

* 1xx: compatibility with older HTTP, typically of no concern
* 2xx: success
* 3xx: redirection (the resource is at another location, or is
  unchanged since last requested)
* 4xx: client errors (the client did something wrong)
* 5xx: server errors (the server failed in a way that was unexpected)

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

Conveying error/fault information to the end user
-------------------------------------------------

**TODO**: We should have a section here that describes the recommended way of
transmitting error/fault information back to the user, including any guidelines
on the payload in the response body.
