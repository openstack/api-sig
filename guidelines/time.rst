Date and Time Conventions
=========================

This topic document serves to provide guidance on how to format dates and times
in the OpenStack public REST APIs.

REST API
--------

* APIs should use ISO 8601 format to return dates and times in resource
  representations. For more information see [1]_.
* It is recommended that the Coordinated Universal Time (UTC) is used to avoid
  differences in time. For more information see [2]_.
* Clients should also use the ISO 8601 format when providing dates to the
  server. The API server should be able to parse and interpret any valid
  ISO 8601 timestamp in any timezone.

.. [1] http://en.wikipedia.org/wiki/ISO_8601
.. [2] http://en.wikipedia.org/wiki/Coordinated_Universal_Time
