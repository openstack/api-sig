.. _metadata:

Metadata
========

This topic document serves to provide guidance on how to work with metadata
in OpenStack REST APIs.

Metadata is sometimes confused with tags. While they have some things in
common, the main function of metadata is to attach additional information,
in the form of key-value pairs, to entities. Tags, on the other side, are
used to classify entities in groups. A separate guidelines document exists
for tags.

For background on the REST guidelines referenced here, see the topic documents
on :ref:`naming` and :ref:`http`.

Metadata Representation
-----------------------

A Python dictionary is used as representation of metadata for a resource. This
dictionary is added as an additional field in the representation of the parent
resource with name ``metadata``.

Example request using a server resource::

    GET /servers/1234567890

Response::

    {
        'id': '1234567890',

        ... other server resource properties ...

        'metadata': {
            "foo": "Foo Value",
            "bar": "Bar Value",
            "baz": "Baz Value"
        }
    }

Updates to the metadata are issued in accordance to the standard HTTP request
methods, issued directly against the parent resource, so for example, to
update the metadata dictionary of a resource, a PUT request should be sent to
the resource, including not only the metadata, but the complete resource
representation in the body. The update in this case does not need to be limited
to metadata, other properties can be updated at the same time.

For resources that have a representation that is not in JSON, a separate
endpoint must be created to expose the metadata. See the "Metadata Resource
URLs" section below for more information.

Character Encoding for Metadata Keys and Values
-----------------------------------------------

Per :rfc:`7159#section-8.1`, JSON documents shall be encoded in UTF-8, UTF-16,
or UTF-32, with UTF-8 being the default and the recommended encoding for
maximum interoperability.

Since the entire metadata representation is a JSON document, the encoding of
the keys and values must match the encoding of the parent document. The use
of UTF-8 encoding is strongly recommended.

Metadata Resource URLs
----------------------

Sometimes it may be inconvenient to work with the metadata portion of a
resource using the complete resource representation, so metadata can also be
exposed as a stand-alone resource. The root resource URL for metadata
management must be the URL of the resource to which the metadata belongs,
followed by */metadata* (for APIs that use user-generated URLs with varying
number of components the */metadata* URL component can be added as a prefix
instead of a suffix).

For example, the resource identified by URL
*http://example.com:8774/servers/1234567890* must expose its metadata with
root URL *http://example.com:8774/servers/1234567890/metadata*.

Obtaining Metadata
~~~~~~~~~~~~~~~~~~

To obtain the metadata for a resource, a GET request must be sent to the root
metadata URL. On success, the server responds with a 200 status code and the
complete set of metadata items in the response body.

Example request::

    GET /servers/1234567890/metadata

Response::

    {
        "metadata": {
            "foo": "Foo Value",
            "bar": "Bar Value",
            "baz": "Baz Value"
        }
    }

Modifying Metadata
~~~~~~~~~~~~~~~~~~

To add, remove, or change metadata items, a PUT request must be sent to the
root metadata URL, with the updated complete list of metadata items in the
body of the request. On success, the server responds with a 200 status code
and the complete updated metadata block in the response body.

.. note:: A PUT request should use etags to avoid the lost update problem.

Example request (updates "foo", removes "bar", adds "qux" and leaves "baz"
untouched)::

    PUT /servers/1234567890/metadata
    {
        "metadata": {
            "foo": "Foo Value Updated",
            "baz": "Baz Value",
            "qux": "Qux Value"
        }
    }

Response::

    {
        "metadata": {
            "foo": "Foo Value Updated",
            "baz": "Baz Value",
            "qux": "Qux Value"
        }
    }

Deleting Metadata
~~~~~~~~~~~~~~~~~

To delete the entire metadata block associated with a resource, a DELETE
request must be sent to the root metadata URL. On success, the server responds
with a 204 status code.

Example request::

    DELETE /servers/1234567890/metadata

To delete multiple metadata items without affecting the remaining ones,
a PUT request must be sent to the root metadata URL with the updated complete
list of metadata items (without items to delete) in the body of the request.
On success, the server responds with a 200 status code.

Example request (removes “foo” and “qux”)::

    PUT /servers/1234567890/metadata
    {
        "metadata": {
            "baz": "Baz Value"
        }
    }

Response::

    {
        "metadata": {
            "baz": "Baz Value"
        }
    }

To delete a single metadata item see below.

Addressing Individual Metadata Items
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As an optional extension to the above, an API can elect to expose additional
endpoints to give clients the ability to work with individual metadata items.
If a project decides to implement this option, then each metadata key-value
pair should be accessed individually at a URL formed by appending the key name
to the root metadata URL. Note that this option is not available for APIs that
use user-generated URLs.

To insert a single metadata item without having to send the entire metadata
block, the client can send a POST request to the root metadata URL, and
include the individual metadata item representation in the request body. On
success, the server responds with a 201 status code and includes the new
metadata item's URL in the ``Location`` header in the response.

Example request::

    POST /servers/1234567890/metadata
    {
        "key": "qux",
        "value": "Qux Value"
    }

Response::

    Location: http://example.com:8774/servers/1234567890/metadata/qux
    {
        "key": "qux",
        "value": "Qux Value",
    }

As shown in the above example, metadata items can be accessed individually by
appending the key name to the root metatadata URL. The representation includes
the key and the value. This format gives APIs the option to include additional
properties that describe a metadata item, such as an expiration date.

To modify an item, a PUT request is sent to the metadata item's URL. On
success, the server responds with a 200 status code and the updated
representation of the metadata item in the response body.

Example request::

    PUT /servers/1234567890/metadata/qux
    {
        "key": "qux",
        "value": "Qux Value Updated"
    }

Response::

    {
        "key": "qux",
        "value": "Qux Value Updated"
    }

To delete a single metadata item without affecting the remaining ones, a
DELETE request is sent to the metadata item URL. On success, the server
responds with a 204 status code.

Example request::

    DELETE /servers/1234567890/metadata/qux
