HTTP Response Codes
===================

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
