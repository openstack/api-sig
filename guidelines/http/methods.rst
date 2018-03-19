HTTP Methods
============

HTTP defines a concept of METHODS on a resource URI.

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
