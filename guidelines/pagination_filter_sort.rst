Pagination, Filtering, and Sorting
==================================

This topic document serves to provide guidance on how to handle the
pagination of large result sets and the best ways to provide filtering
and sorting capabilities in a project's public REST API.

Pagination
----------

**TODO** Discuss the methods currently used to paginate in OpenStack APIs.

**TODO** Make a proposal/decision on the recommended way to implement
pagination.

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
parameters. To avoid conflicts, filter parameters are prefixed with ``f_``.
This is important to be able to filter on fields like ``limit`` and ``marker``.
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

  GET /app/items?f_foo=buzz
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
``/app/items?f_foo=buzz&f_baz=quux`` would provide no results.

**IN** operations are available for single fields, using comma-separated
options for the field value and colon separation for the ``in``
operator. The value must be in the list of values provided for the query
to succeed.::

  GET /app/items?f_foo=in:buzz,bar
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
``?f_foo=in:"a,bc",d``. If values contain double-quotes, those can be
backslashed inside quotes. For a value ``a"b"c`` the query would be
``?f_foo="a\"b\"c"``.

For queries that need comparisons other than simple equals, operators are
supported for membership, inequality, greater-than, greater-than-or-equal,
less-than, and less-than-or-equal-to. In order, the operators are: ``in``,
``neq``, ``gt``, ``gte``, ``lt``, and ``lte``. Simple equality is the default
operation, and is performed as ``?f_param=foo``.

They can be used in queries compounded with the values they work on. For
example, finding objects with a size greater than 8 would be written as
``?f_size=gt:8`` and would return::

  GET /app/items?f_size=gt:8
  {
    "items": [
      {
        "foo": "bar",
        "baz": "quux",
        "size": 9
      }
    ]
  }

Operators must be followed by colons, so the query ``?f_foo=gte`` searches for
the literal string "gte" and searching for "gte:" can be done by quoting the
value as ``?f_foo="gte:"``.

**TODO:** Add guidance on a "LIKE" or regex operator to search text.

Paginating responses should be done *after* applying the filters in a query,
because it's possible for there to be no matches in the first page of results,
and returning an empty page is a poor API when the user explicitly requested a
number of results.

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
