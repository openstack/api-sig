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

* For all other successful requests, the return code should be **200 OK**.

* If a request attempts to put a resource into a state which it is
  already in (eg locking an instance which is already locked), the return code
  should be in the **2xx Successful** range (usually matching the return code
  which would be given if the state had changed). It is not appropriate to use
  **409 Conflict** when the resulting state of the resource is as the user
  requested.

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

Failure Code Clarifications
~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
  some action to fix. It is also possible that this error can be raised
  deliberately in case of some detected but unrecoverable error such as failure
  to communicate with another service component, eg MessageQueueTimeout,
  IOError caused by a full disk, etc.

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
  accept missing resource fields as unchanged. This is valid under :rfc:`5789`,
  but makes it possible to lose updates when dealing with lists or sets.

* GET method

 * GET method should be used only for getting information of resources, and it
   should not change resources' state at all because :rfc:`7231` mentions **GET
   is the primary mechanism of information retrieval and the focus of almost
   all performance optimizations.**.

HTTP request bodies are theoretically allowed for all methods except TRACE,
however they are not commonly used except in PUT, POST and PATCH. Because of
this, they may not be supported properly by some client frameworks and we
would discourage API methods from accepting request bodies for GET, DELETE,
TRACE, OPTIONS and HEAD methods.

Conveying error/fault information to the end user
-------------------------------------------------

**TODO**: We should have a section here that describes the recommended way of
transmitting error/fault information back to the user, including any guidelines
on the payload in the response body.
