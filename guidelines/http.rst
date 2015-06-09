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

HTTP Caching and Proxy Behavior
-------------------------------

HTTP was designed to be proxied and cached heavily. HTTP caching by
both intermediary proxies, and by clients themselves, is to be
expected in all cases where it is allowed. This is a fundamental
design point to allow HTTP to work at high scale.

That means that whenever a response is defined as cacheable, for any
reason, the server implementation should assume that those responses
will be cached. This could mean that the server **will never see**
follow up requests if it does not specify appropriate Cache-Control
directives on cacheable responses.

The following HTTP methods are defined as cacheable: HEAD, GET, and
POST :rfc:`7231#section-4.2.3` (section 4.2.3).

Requests that return a status code of any of the following are defined
as cacheable: 200, 203, 204, 206, 300, 301, 404, 405, 410, 414, and
501 :rfc:`7231#section-6.1` (section 6.1).

Most Python HTTP client libraries are extremely conservative on
caching, so a whole class of completely valid RFC caching won't be
seen when using these clients. Assuming "it works in the Python
toolchain" does not mean that it will in all cases, or is the only way
to implement the HTTP. We expect that in-browser javascript clients
will have vastly different cache semantics (that are completely valid
by the RFC) than the existing Python clients.

Thinking carefully about cache semantics when implementing anything
in the OpenStack API is critical to the API being compatible with the
vast range of runtimes, programming languages, and proxy servers (open
and commercial) that exist in the wild.

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

HTTP defines a concept of METHODS on a resource uri.

..

 +-------------+--------------+--------------------+--------------------+
 | METHOD      | URI          | ACTION             | HAS BODY?          |
 +-------------+--------------+--------------------+--------------------+
 | HEAD        | /foo/ID      | EXISTS             | NO                 |
 +-------------+--------------+--------------------+--------------------+
 | GET         | /foo/ID      | READ               | NO                 |
 +-------------+--------------+--------------------+--------------------+
 | POST        | /foo         | CREATE             | YES                |
 +-------------+--------------+--------------------+--------------------+
 | PUT         | /foo/ID      | UPDATE             | YES                |
 +-------------+--------------+--------------------+--------------------+
 | PATCH       | /foo/ID      | UPDATE (partial)   | YES                |
 +-------------+--------------+--------------------+--------------------+
 | DELETE      | /foo/ID      | DELETE             | NO                 |
 +-------------+--------------+--------------------+--------------------+

This looks close to a CRUD mapping, but it's important to realize the
defining characteristic of POST isn't that it creates items, but that
you POST to a URI that's different than the resource you get
back. POST is therefor also appropriate for bulk operations like
multiple update, or triggering some arbitrary other actions beyond
resource creation (i.e. reboot a server).

**TODO**: HEAD is weird in a bunch of our wsgi frameworks and you
don't have access to it. Figure out if there is anything useful
there.

**TODO**: Provide guidance on what HTTP methods (PUT/POST/PATCH/DELETE, etc)
should always be supported, and which should be preferred.

Conveying error/fault information to the end user
-------------------------------------------------

**TODO**: We should have a section here that describes the recommended way of
transmitting error/fault information back to the user, including any guidelines
on the payload in the response body.

Common Mistakes
---------------

There are many common mistakes that have been made in the
implementations of RESTful APIs in OpenStack. This section attempts to
enumerate them with reasons why they were wrong, and propose future
alternatives.

Use of 501 - Not Implemented
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some time in the Folsom era projects started using 501 for "Feature
Not Implemented" - `Discussion on openstack-dev
<http://lists.openstack.org/pipermail/openstack-dev/2012-December/003759.html>`_

This is a completely incorrect reading of HTTP. "Method" means
something very specific in HTTP, it means an HTTP Method. One of GET /
HEAD / POST / PUT / PATCH / OPTIONS / TRACE.

The purpose of the 501 error was to indicate to the client that POST
is not now, and never will be an appropriate method to call on any
resource on the server. An appropriate client action is to blacklist
POST and ensure no code attempts to use this. This comes from the
early days of HTTP where there were hundreds of commercial HTTP server
implementations, and the assumption that all HTTP methods would be
handled by a server was not something the vendors could agree on. This
usage was clarified in RFC :rfc:`7231#section-6.6.2` (section 6.6.2).

If we assume the following rfc statement to be true: "This is the
appropriate response when the server does not recognize the request
method and is not capable of supporting it for any resource." that is
irreconcilable with a narrower reading, because we've said all clients
are correct in implementing "never send another POST again to any
resource". It's as if saying the "closed" sign on a business means
both, closed for today, as well as closed permanently and ok for the
city to demolish the building tomorrow. Stating that either is a valid
reading so both should be allowed only causes tears and confusion.

We live in a very different world today, dominated by Apache and
Nginx. As such 501 is something you'd be unlikely to see in the
wild. However that doesn't mean we can replace it's definition with
our own.

Going forward projects should use a 400 'BadRequest' response for this
condition, plus a more specific error message back to the user that
the feature was not implemented in that cloud. 404 'NotFound' may also
be appropriate in some situations when the URI will never
exist. However one of the most common places where we would return
"Feature Not Implemented" is when we POST an operation to a URI of the
form /resource/{id}/action. Clearly that URI is found, however some
operations on it were not supported. Returning a 404 (which is by
default cachable) would make the client believe /resource/{id}/action
did not exist at all on the server.
