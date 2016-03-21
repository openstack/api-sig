Counting Resources
==================

This topic document serves to provide guidance on returning the total size of
a resource collection in a project's public REST API; this is useful when the
total number of resources may be larger than the number of resources being
enumerated in a single response.

Guidance
--------

The 'with_count' query string parameter is used to indicate if the total count
of resources should or should not be returned from a GET REST API request. Any
value that equates to True indicates that the count should be returned;
conversely, any value that equates to False indicates that the count should
not be returned.

If the 'with_count' query string parameter is absent, the server may still
include the count; however, it should only do so if determining the count is
trivial and does not require, for example, an additional database query. When
the count is potentially expensive to obtain, it should only be included if it
is explicitly requested.

In the JSON reply, the count value is an integer and is associated with the
top-level property 'count'. For example, when retrieving servers, if
'with_count=true' is supplied then the total count should be included in the
reply as::

    {
        "servers": [...],
        "count": <int_count>
    }
