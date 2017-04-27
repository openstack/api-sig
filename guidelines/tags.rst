.. _tags:

Tags
====

This topic document serves to provide guidance on how to work with tags in
OpenStack REST APIs.

Tags are often confused with metadata. While the two have an intersection, the
main function of tags is to classify a collection of entities in groups, while
metadata is used to attach additional information to entities. A separate
guideline document exists for metadata.

For background on the REST guidelines referenced here, see the topic documents
on :ref:`naming` and :ref:`http`.

Tags Representation
-------------------

Tags are strings attached to an entity with the purpose of classification into
groups.

An entity can have zero, one or more tags associated with it, for that
reason the recommended representation within the parent entity is a list.

Example request using a server resource::

    GET /servers/1234567890

Response::

    {
        'id': '1234567890',

        ... other server resource properties ...

        'tags': ['foo', 'bar', 'baz']
    }

Updates to the tags are issued in accordance to the standard HTTP request
methods, issued directly against the parent resource. To update the tag list
of a resource, a PUT request should be sent to the resource, including not only
the updated tag list, but the complete resource representation in the body. The
update in this case does not need to be limited to tags, other properties can
be updated at the same time. Note that by using a PUT request it is possible to
add and/or remove multiple tags in one single operation, simply by sending
the updated tag list with the resource representation.

For resources that have a representation that is not in JSON a separate
endpoint must be created to expose the tags. See the "Tag Resource URLs"
section below for more information.

Tags Restrictions
-----------------

Tags are strings with the following basic restrictions:

* Tags are case sensitive.
* '/' is **not** allowed to be in a tag name
* Comma is **not** allowed to be in a tag name in order to simplify requests
  that specify lists of tags
* All other characters are allowed to be in a tag name

.. note::

    The '/' character is forbidden because some servers have a problem with
    encoding this character. The problem is that the server will handle '%2F'
    as '/' even though '/' is encoded. It's a problem of poor server
    implementation. To avoid problems with handling URLs character '/' is
    forbidden in tag names.

Character Encoding for Tags
---------------------------

Per :rfc:`7159#section-8.1`, JSON documents shall be encoded in UTF-8, UTF-16,
or UTF-32, with UTF-8 being the default and the recommended encoding for
maximum interoperability.

Since the tags are part of a JSON document, the encoding of the tag names must
match the encoding of the parent document. The use of UTF-8 encoding is
strongly recommended.

Tags Resource URLs
------------------

Sometimes it may be inconvenient to work with the tags portion of a resource
using the complete resource representation, so tags can optionally be exposed
as a stand-alone resource as well. If a project decides to provide this
functionality, then the root resource URL for tag management should be
the URL of the resource to which the tags belong, followed by */tags* (for
APIs that use user-generated URLs with varying number of components the *tags/*
URL component can be added as a prefix instead of a suffix).

For example, the resource identified by URL
*http://example.com:8774/servers/1234567890* must expose its tags with
root URL *http://example.com:8774/servers/1234567890/tags*.

Obtaining the Tag List
~~~~~~~~~~~~~~~~~~~~~~

To obtain the tags for a resource, a GET request must be sent to the root
tags URL. On success, the server responds with a 200 status code and the
complete set of tags items in the response body.

Example request::

    GET /servers/1234567890/tags

Response::

    {
        "tags": ['foo', 'bar', 'baz']
    }

Note that this representation differs from the one adopted by Nova. One reason
is that with this structure it is possible to add additional metadata to the
request body. A secondary reason is that JSON arrays as a top level entity
have been found to expose vulnerabilities in browsers, as reported by the
following articles:

- http://haacked.com/archive/2008/11/20/anatomy-of-a-subtle-json-vulnerability.aspx/
- http://haacked.com/archive/2009/06/25/json-hijacking.aspx/

Modifying the Tag List
~~~~~~~~~~~~~~~~~~~~~~

To add, remove, or change tags, a PUT request should be sent to the
root tags URL, with the updated complete list of tags in the body of the
request. On success, the server responds with a 200 status code and the
complete updated tag list in the response body.

Example request (removes "bar" and adds "qux")::

    PUT /servers/1234567890/tags
    {
        "tags": ['foo', 'baz', 'qux']
    }

Response::

    {
        "tags": ['foo', 'baz', 'qux']
    }

If the number of tags exceeds the limit allowed by the API, the return code
should be **400 Bad Request** as the HTTP Guidelines describe. To achieve
request success, the client should change the requested number of tags to
be less than the API limit.

Deleting Tags
~~~~~~~~~~~~~

To delete the entire tag list associated with a resource, a DELETE
request must be sent to the root tags URL. On success, the server responds
with a 204 status code.

Example request::

    DELETE /servers/1234567890/tags

Addressing Individual Tags
~~~~~~~~~~~~~~~~~~~~~~~~~~

To provide even more fine-grained access to tags, another optional extension is
to expose resource URLs for individual tags. If a project decides to implement
this option, then each tag should be accessed individually at a URL formed by
appending the tag name to the root tag URL. Note that this option is not
available for APIs that use user-generated URLs.

To insert a single tag without having to send the entire tag list, the client
should send a PUT request to the inidividual tag URL. On success, the server
responds with a 201 status code and includes the new tag's URL in the
``Location`` header in the response.

Example request::

    PUT /servers/1234567890/tags/qux
    <no body>

Response::

    Location: http://example.com:8774/servers/1234567890/tags/qux
    <no body>

To check if a tag exists or not, the client should send a HEAD request to the
individual tag URL. If the tag exists, the server responds with a status code
204 and no response body. If the tag does not exist, the server responds with
a status code 404.

To delete a single tag without affecting the remaining ones, a
DELETE request is sent to the individual tag URL. On success, the server
responds with a 204 status code. If an invalid tag is given, a 404 response
is returned.

Example request::

    DELETE /servers/1234567890/tags/qux

Filtering and Searching by Tags
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To search the collection of entities by their tags, the client should send a
GET request to the collection URL, and include query string parameters that
define the query. These arguments can be combined with other arguments, such
as those that perform additional filtering outside of tags, pagination,
sorting, etc. The recommended query string arguments for filtering tags are
``tags``, ``tags-any``, ``not-tags`` and ``not-tags-any``.

Note that once again this is different than the nova specification, which
uses repeated ``tag`` query arguments to specify a list of tags. The preference
here is to be consistent with the sorting guideline document, for which it
was decided that repeating query string arguments is not a good idea due to
not having good support among web clients and servers.

To request the list of entities that have a single tag, ``tags`` argument
should be set to the desired tag name. Example::

    GET /servers?tags=red

To request the list of entities that have two or more tags, the ``tags``
argument should be set to the list of tags, separated by commas. In this
situation the tags given must all be present for an entity to be included in
the query result. Example that returns servers that have the "red" and "blue"
tags::

    GET /servers?tags=red,blue

To request the list of entities that have one or more of a list of given tags,
the ``tags-any`` argument should be set to the list of tags, separated by
commas. In this situation as long as one of the given tags is present the
entity will be included in the query result. Example that returns the servers
that have the "red" or the "blue" tag::

    GET /servers?tags-any=red,blue

To request the list of entities that do not have one or more tags, the
``not-tags`` argument should be set to the list of tags, separated by commas.
In this situation only the entities that do not have any of the given tags will
be included in the query results. Example that returns the servers that do not
have the "red" nor the "blue" tag::

    GET /servers?not-tags=red,blue

To request the list of entities that do not have at least one of a list of
tags, the ``not-tags-any`` argument should be set to the list of tags,
separated by commas. In this situation only the entities that do not have at
least one of the given tags will be included in the query result. Example that
returns the servers that do not have the "red" tag, or do not have the "blue"
tag::

    GET /servers?not-tags-any=red,blue

The ``tags``, ``tags-any``, ``not-tags`` and ``not-tags-any`` arguments can be
combined to build more complex queries. Example::

    GET /servers?tags=red,blue&tags-any=green,orange

The above example returns any servers that have the "red" and "blue" tags, plus
at least one of "green" and "orange".

It is possible to create a request which is self-contradictory. Example::

    GET /servers?tags=red&not-tags=red

This should be treated as a valid request (ie *not* a client error), and should
return an empty result-set with a 2xx status code.
