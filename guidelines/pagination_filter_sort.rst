Pagination, Filtering, and Sorting
==================================

This topic document serves to provide guidance on how to handle the
pagination of large result sets and the best ways to provide filtering
and sorting capabilities in a project's public REST API.

Pagination
----------

Pagination can be implemented using one or both of two query parameters:

- ``limit`` to define the number of items returned in the response, and

- ``marker`` to specify the ID of the last seen item

Note that the marker need not always be the ID/UUID field of the record; it can
be any field or combination of fields that will uniquely identify that record.
Using a marker that is not unique will result in overlap or skipped records
between paged results.

For example::

  GET /app/items?limit=30

Would return *at most* 30 items::

  {
    "items": [
      {
        "id": "719aae5f70db4364850f6198ea874aa6",
        "foo": "bar",
        "baz": "quux",
        "size": 9
      },
      ...
      {
        "id": "08ec231f6d9a43dda97d4b950c3393df",
        "foo": "buzz",
        "baz": "honk",
        "size": 6
      }
    ]
  }

If, we then wanted to request the next 30 items after the last one, we would
do::

  GET /app/items?limit=30&marker=08ec231f6d9a43dda97d4b950c3393df

This would return the next (at most) 30 items after the item with ID
``08ec231f6d9a43dda97d4b950c3393df``.

The ability to page through results implies that the items are sorted in a
consistent fashion in each request, even if that order is nothing more than the
order the items were added to the dataset. If the order of the results changes
between requests, the returned pages will not have a meaningful relation to
each other.

A similar consideration would be how to handle the situation when the item
whose ID is the ``marker`` value is deleted in between requests. In that event,
the response should start with the next item logically. The definition of
"logical" is necessarily fuzzy, and will depend on how the data is sorted.
There may be some cases, however, where it is not reasonable to try to
determine what the next logical item would be. In those cases, a **400 Bad
Request** response should be returned, with a clear explanation in the error
message that the requested marker value does not exist.

It is also helpful to users if services generate pagination links and include
them in the :ref:`links` portion of the response body. Providing the following
link types will make pagination navigation easier:

- first
- prev
- self
- next
- last

It is important to note that unless the data being paged is static, these links
cannot be guaranteed to be accurate. For example, if some items are deleted,
the ``prev`` link might contain some items from the current result.

For example, a response to::

  GET /app/items?limit=30&marker=752b0b9997f24be49e5a1d89d1c53279

Would look more akin to::


  {
    "items": [
      {
        "id": "719aae5f70db4364850f6198ea874aa6",
        "foo": "bar",
        "baz": "quux",
        "size": 9
      },
      ...
      {
        "id": "08ec231f6d9a43dda97d4b950c3393df",
        "foo": "buzz",
        "baz": "honk",
        "size": 6
      }
    ],
    "links": [
        {
            "rel": "self",
            "href": "http://example.com/app/items?limit=30&marker=752b0b9997f24be49e5a1d89d1c53279",
        },
        {
            "rel": "first",
            "href": "http://example.com/app/items?limit=30",
        },
        {
            "rel": "prev",
            "href": "http://example.com/app/items?limit=30&marker=eff79f5b4f8743caa1f775846302c1d5",
        },
        {
            "rel": "next",
            "href": "http://example.com/app/items?limit=30&marker=08ec231f6d9a43dda97d4b950c3393df",
        },
        {
            "rel": "last",
            "href": "http://example.com/app/items?limit=30&marker=6835afb7ea29491bb2722c6c43f1f070",
        }
    ]
  }

Alternatively, if services are not including JSON `Hyper-Schema`_ links in
their responses they can consider using the ``Link`` header as defined in
:rfc:`5988` and :rfc:`6903`.

When using links, the links that are included change based on which page the
user requested. For example, if the user has requested the first page, then it
still makes sense to include ``first``, ``self``, ``next``, and ``last`` but
not ``prev``. Likewise if it is the last page, then including ``next`` is
optional but the rest (``first``, ``prev``, ``self``, ``last``) is sensible.

It should also be emphasized that calculating the ``last`` link can be costly.
In many cases, such link calculation would require querying the entire dataset.
Therefore implementing the ``last`` link is optional.

Filtering
---------

Filtering can be implemented as a query parameter named for the field to be
filtered on, the value should (naturally) be the value you need to filter for.

An existing example of filtering in
`Nova <http://specs.openstack.org/openstack/neutron-specs/specs/api/networking_general_api_information.html#filtering-and-column-selection>`_
It is notable that Nova doesn't support OR filters, requiring
separate requests per query.

A different strategy is to specify query objects and pass them as a single
URL-encoded JSON list. This is less client-friendly because it requires extra
encoding steps.

The simplest way to allow filtering is to map filterable parameters to query
parameters.
Take the sample object::

  GET /app/items
  {
    "items": [
      {
        "foo": "bar",
        "baz": "quux",
        "size": 9
      },
      {
        "foo": "buzz",
        "baz": "honk",
        "size": 6
      }
    ]
  }

To filter on a field, simply add that field and its value to the query.::

  GET /app/items?foo=buzz
  {
    "items": [
      {
        "foo": "buzz",
        "baz": "honk",
        "size": 9
      }
    ]
  }

Multiple filters result in an implicit AND, so in our example
``/app/items?foo=buzz&baz=quux`` would provide no results.

**IN** operations are available for single fields, using comma-separated
options for the field value and colon separation for the ``in``
operator. The value must be in the list of values provided for the query
to succeed.::

  GET /app/items?foo=in:buzz,bar
  {
    "items": [
      {
        "foo": "bar",
        "baz": "quux",
        "size": 9
      },
      {
        "foo": "buzz",
        "baz": "honk",
        "size": 6
      }
    ]
  }

If values contain commas, they can be quoted similar to CSV escaping. For
example, a query for the value ``a,bc`` or ``d`` would be
``?foo=in:"a,bc",d``. If values contain double-quotes, those can be
backslashed inside quotes. Newline ("\n") and carriage return ("\r") escapes
are also allowed. Actual backslashes must be doubled. For a value ``a"b\c``
the query would be ``?foo="a\"b\\c"``. Unquoted values may not contain quotes
and backslashes are treated as any other character. So for a value ``a\b``
the query would be ``?foo=a\b``.

For queries that need comparisons other than simple equals, operators are
supported for membership, non-membership, inequality, greater-than,
greater-than-or-equal, less-than, and less-than-or-equal-to. In order, the
operators are: ``in``, ``nin``, ``neq``, ``gt``, ``gte``, ``lt``, and ``lte``.
Simple equality is the default operation, and is performed as ``?param=foo``.

They can be used in queries compounded with the values they work on. For
example, finding objects with a size greater than 8 would be written as
``?size=gt:8`` and would return::

  GET /app/items?size=gt:8
  {
    "items": [
      {
        "foo": "bar",
        "baz": "quux",
        "size": 9
      }
    ]
  }

Operators must be followed by colons, so the query ``?foo=gte`` searches for
the literal string "gte" and searching for "gte:" can be done by quoting the
value as ``?foo="gte:"``.

**TODO:** Add guidance on a "LIKE" or regex operator to search text.

Paginating responses should be done *after* applying the filters in a query,
because it's possible for there to be no matches in the first page of results,
and returning an empty page is a poor API when the user explicitly requested a
number of results.

Time based filtering queries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To support filtering based on time intervals such as mentioned in the `ISO8601
intervals wikipedia page`_, it should be possible to express the following
use cases through API queries:

* a two-ISO8601-date timestamp interval
* an open-ended, single-ISO8601-date interval
* multiple time intervals an item may belong to
* equality with a default value where no time has been set yet

.. _ISO8601 intervals wikipedia page:  https://en.wikipedia.org/wiki/ISO_8601#Time_intervals

For instance, the `Ironic Inspector`_ project keeps track of node introspection
statuses that include the ``started_at`` and ``finished_at`` fields. While the
former value is always present, the latter is present only if the introspection
finished::

  GET /app/item
  {
    "items": [
      {"id": "item1", "started_at": "2016-10-10T15:00Z",
       "finished_at": "2016-10-10T15:30Z"},
      {"id": "item2", "started_at": "2016-10-10T15:15Z",
       "finished_at": "2016-10-10T16:00Z"},
      {"id": "item3", "started_at": "2016-10-10T15:45Z",
       "finished_at": null}
    ]
  }

.. _Ironic Inspector: http://docs.openstack.org/developer/ironic-inspector/

To obtain items that finished between 15:30 and 16:00 UTC Today use an
interval with two boundaries::

  GET /app/items?finished_at=ge:15:30&finished_at=lt:16:00
  {
    "items": [
      {"id": "item1", "started_at": "2016-10-10T15:00Z",
       "finished_at": "2016-10-10T15:30Z"}
    ]
  }

To list items that finished any time after 15:30 UTC Today, use an
open-ended time interval query::

  GET /app/items?finished_at=ge:15:30
  {
    "items": [
      {"id": "item1", "started_at": "2016-10-10T15:00Z",
       "finished_at": "2016-10-10T15:30Z"},
      {"id": "item2", "started_at": "2016-10-10T15:15Z",
       "finished_at": "2016-10-10T16:00Z"}
    ]
  }

Finally, to include items that didn't finish yet, use the default value
equality. Since the queries are implicitly AND-ed, use two requests::

  GET /app/items?finished_at=ge:16:00
  {
    "items": [
      {"id": "item2", "started_at": "2016-10-10T15:15Z",
       "finished_at": "2016-10-10T16:00Z"}
    ]
  }
  GET /app/items?finished_at=null
  {
    "items": [
      {"id": "item3", "started_at": "2016-10-10T15:45Z",
       "finished_at": null}
    ]
  }


Sorting
-------

Sorting is determined through the use of the 'sort' query string parameter. The
value of this parameter is a comma-separated list of sort keys. Sort directions
can optionally be appended to each sort key, separated by the ':' character.

The supported sort directions are either 'asc' for ascending or 'desc' for
descending.

The caller may (but is not required to) specify a sort direction for each key.
If a sort direction is not specified for a key, then a default is set by the
server.

For example:

- Only sort keys specified:

  + ``sort=key1,key2,key3``
  + 'key1' is the first key, 'key2' is the second key, etc.
  + Sort directions are defaulted by the server

- Some sort directions specified:

  + ``sort=key1:asc,key2,key3``
  + Any sort key without a corresponding direction is defaulted
  + 'key1' is the first key (ascending order), 'key2' is the second key
    (direction defaulted by the server), etc.

- Equal number of sort keys and directions specified:

  + ``sort=key1:asc,key2:desc,key3:asc``
  + Each key is paired with the corresponding direction
  + 'key1' is the first key (ascending order), 'key2' is the second key
    (descending order), etc.

Note that many projects have implemented sorting using repeating 'sort_key'
and 'sort_dir' query string parameters, see [1]. As these projects adopt these
guidelines, they should deprecate the older parameters appropriately.

[1]: https://wiki.openstack.org/wiki/API_Working_Group/Current_Design/Sorting


.. _Hyper-Schema:
    http://json-schema.org/latest/json-schema-hypermedia.html
