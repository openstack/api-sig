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

**TODO** Discuss the methods currently used to filter in OpenStack APIs.

**TODO** Make a proposal/decision on the recommended way to implement
filtering.

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
