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

A common misconception is that requests issued over a secure HTTP connection
are not cached for security reasons. In fact, there is no exception made for
https in the HTTP specification, caching works in exactly the same way as for
non-encrypted HTTP. Most modern browsers apply the same caching algorithm to
secure connections.

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

HTTP Links
----------

Including links to resources are an important part of any HTTP API. Links in
OpenStack APIs conform to the :ref:`links` guideline.

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

* For all other successful requests, the return code should be **200 OK**.

* If a request attempts to put a resource into a state which it is
  already in (for example, locking an instance which is already locked), the
  return code should be in the **2xx Successful** range (usually matching the
  return code which would be given if the state had changed). It is not
  appropriate to use **409 Conflict** when the resulting state of the resource
  is as the user requested.

5xx Server Error Codes
~~~~~~~~~~~~~~~~~~~~~~

These codes represent that the server, or gateway, has encountered an error
or is incapable of performing the requested method. They indicate to a
client that the request has resulted in an error that exists on the
server side and not with the client.

They should be used to indicate that errors have occurred during the
request process which cannot be resolved by the client alone. The nature
of each code in the 5xx series carries a specific meaning and they should
be fully researched before deploying.

The server **must not** return server-side stacktraces/traceback output to the
end user. Tracebacks and stacktraces belong in server-side logs, not returned
via the HTTP API to an end user.

Failure Code Clarifications
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* If the request results in the OpenStack user exceeding his or her quota, the
  return code should be **403 Forbidden**. Do **not** use **413 Request
  Entity Too Large**.

* For badly formatted requests, the return code should be **400 Bad Request**.
  Do **not** use **422 Unprocessable Entity**.

  * If the API limits the length of a property that is a collection, the return
    code should be **400 Bad Request** when the request exceeds the length
    limit. The client should adjust requests to achieve success, and shouldn't
    expect to repeat the request and have it work. Do **not** use
    **403 Forbidden** for this case, because this is different than exceeding
    quota -- for a subsequent request to succeed when quotas are exceeded the
    server environment must change.

* If a request contains a reference to a nonexistent resource in the body
  (not URI), the code should be **400 Bad Request**. Do **not** use **404
  NotFound** because :rfc:`7231#section-6.5.4` (section 6.5.4) mentions **the
  origin server did not find a current representation for the target resource**
  for 404 and **representation for the target resource** means a URI. A good
  example of this case would be when requesting to resize a server to a
  non-existent flavor. The server is the resource in the URI, and as long as it
  exists, 404 would never be the proper response. **422 Unprocessable Entity**
  is also an option for this situation but do **not** use 422 because the code
  is not defined in :rfc:`7231` and not standard. Since the 400 response code
  can mean a wide range of things, it is extremely important that the error
  message returned clearly indicates that the resource referenced in the body
  does not exist, so that the consumer has a clear understanding of what they
  need to do to correct the problem.

* If a request contains an unexpected attribute in the body, the server should
  return a **400 Bad Request** response. Do **not** handle the request as
  normal by ignoring the bad attribute. Returning an error allows the client
  side to know which attribute is wrong and have the potential to fix a bad
  request or bad code. (For example, `additionalProperties` should be `false`
  on JSON-Schema definition)

* Similarly, if the API supports query parameters and a request contains an
  unknown or unsupported parameter, the server should return a **400 Bad
  Request** response. Invalid values in the request URL should never be
  silently ignored, as the response may not match the client's expectation. For
  example, consider the case where an API allows filtering on name by
  specifying '?name=foo' in the query string, and in one such request there is
  a typo, such as '?nmae=foo'. If this error were silently ignored, the user
  would get back all resources instead of just the ones named 'foo', which
  would not be correct.  The error message that is returned should clearly
  indicate the problem so that the user could correct it and re-submit.

* If a request is made to a known resource URI, but the HTTP method used for
  the request is not supported for that resource, the return code should be
  **405 Method Not Allowed**. The response should include the `Allow` header
  with the list of accepted request methods for the resource.

* If a request is made which attempts to perform an action on a resource which
  is already performing that action and therefore the request cannot be
  fulfilled (for example, snapshotting an instance which is already in the
  process of snapshotting), the return code should be **409 Conflict**.

* A **500 Internal Server Error** should **not** be returned to the user for
  failures due to user error that can be fixed by changing the request on the
  client side.  500 failures should be returned for any error state that cannot
  be fixed by a client, and requires the operator of the service to perform
  some action to fix. It is also possible that this error can be raised
  deliberately in case of some detected but unrecoverable error such as a
  MessageQueueTimeout from a failure to communicate with another service
  component, an IOError caused by a full disk, or similar error.

.. note:: If an error response body is returned, it must conform to the
   :ref:`errors` guideline.

HTTP Methods
------------

HTTP defines a concept of METHODS on a resource uri.

..

 +-------------+--------------+--------------------+--------------------+
 | METHOD      | URI          | ACTION             | HAS REQUEST BODY?  |
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

The mapping of HTTP requests method to the Create, Read, Update, Delete
(`CRUD
<https://en.wikipedia.org/wiki/Create,_read,_update_and_delete>`_) model
is one of convenience that can be considered a useful, but incomplete,
memory aid. Specifically it misrepresents the meaning and purpose
of POST. According to :rfc:`7231#section-4.3.3` POST "requests that
the target resource process the representation enclosed in the request
according to the resource's own specific semantics". This can, and
often does, mean create but it can mean many other things, based on
the resource's requirements.

More generally, CRUD models the four basic functions of persistent
storage. An HTTP API is not solely a proxy for persistent storage.
It can provide access to such storage, but it can do much more.

Please note that while HEAD is recommended for checking for the existence of a
resource, the corresponding GET should always be implemented too, and should
return an identical response with the addition of a body, if applicable.

**TODO**: HEAD is weird in a bunch of our wsgi frameworks and you
don't have access to it. Figure out if there is anything useful
there.

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

* There can also be confusion on when to use **POST** or **PUT** in the
  specific instance of creating new resources. **POST** should be used when
  the URI of the resulting resource is different from the URI to which the
  request was made and results in the resource having an identifier (the URI)
  that the server generated. In the OpenStack environment this is the common
  case. **PUT** should be used for resource creation when the URI to which the
  request is made and the URI of the resulting resource is the same.

  That is, if the id of the resource being created is known, use **PUT** and
  **PUT** to the correct URI of the resource. Otherwise, use **POST** and
  **POST** to a more generic URI which will respond with the new URI of the
  resource.

* The **GET** method should only be used for retrieving representations of
  resources. It should never change the state of the resource identified by
  the URI nor the state of the server in general. :rfc:`7231#section-4.3.1`
  states **GET is the primary mechanism of information retrieval and the
  focus of almost all performance optimizations.**.

HTTP request bodies are theoretically allowed for all methods except TRACE,
however they are not commonly used except in PUT, POST and PATCH. Because of
this, they may not be supported properly by some client frameworks, and you
should not allow request bodies for GET, DELETE, TRACE, OPTIONS and HEAD
methods.

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
