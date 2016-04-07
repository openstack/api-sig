.. _microversion_specification:

Microversion Specification
==========================

This topic document serves to provide guidance on how to work with
microversions in OpenStack REST APIs.

Microversions enables the ability to introduce API changes while being able
to allow clients to discover those changes. According to negotiations with
servers, clients adjust their behavior to work with server correctly.

Versioning
----------

TBD

Client Interaction
------------------

A client specifies the version of the API they want via the following
approach, a new header::

  OpenStack-API-Version: [SERVICE_TYPE] 2.114

For example, Keystone will use the header::

  OpenStack-API-Version: identity 2.114

This conceptually acts like the accept header.

Clients should expect the following behavior from the server:

* If the OpenStack-API-Version header is not provided, act as if
  the minimum supported version was specified.

* If the OpenStack-API-Version header is sent, but the value does
  not match the current service, act as if the minimum supported
  version was specified.

* If the OpenStack-API-Version header is sent, the service type
  matches, and the version takes the form of a version string respond
  with the API at the indicated version. If the version is outside the
  range of versions supported and is not the string ``latest`` (as
  described below), return 406 Not Acceptable, and a response body
  including the supported minimum and maximum versions.

* If OpenStack-API-Version header is sent, the service type matches, and
  the version is set to the special keyword ``latest`` behave as if
  maximum version was specified.

.. warning:: The ``latest`` value is mostly meant for integration testing and
  would be dangerous to rely on in client code since microversions are not
  following `semver <http://semver.org/>`_ and therefore backward compability
  is not guaranteed. Clients should always require a specific microversions but
  limit what is acceptable to the version range that it understands at the
  time.

Two extra headers are always returned in the response::

    OpenStack-API-Version: [SERVICE_TYPE] version_number
    Vary: OpenStack-API-Version

The first header specifies the version number of the API which was
executed. An example::

    OpenStack-API-Version: compute 2.22

The ``Vary`` header is used as a hint to caching proxies and user
agents that the response is also dependent on the OpenStack-API-Version
and not just the body and query parameters. See
:rfc:`7231#section-7.1.4` for details.

.. note:: Servers must be prepared to deal with multiple
  OpenStack-API-Version headers. This could happen when a client
  designed to address multiple services always sends the headers it
  thinks it needs. Most Python frameworks will handle this by setting
  the value of the header to the values of all matching headers,
  joined by a ',' (comma). For example ``compute 2.11,identity
  2.114``.


Version Discovery
-----------------

The Version API for each service should return the minimum and maximum
versions. These values are used by the client to discover the supported API
versions.

A version response would look as follows. This example is from the compute API
provided by Nova::

    GET /
    {
         "versions": [
            {
                "id": "v2.1",
                "links": [
                      {
                        "href": "http://localhost:8774/v2/",
                        "rel": "self"
                    }
                ],
                "status": "CURRENT",
                "max_version": "5.2",
                "min_version": "2.1"
            },
       ]
    }

"max_version" is maximum version, "min_version" is minimum version.

When the requested version is out of range for the server, the server returns
status code **406 Not Acceptable** along with a response body.

The error response body conforms to the errors guideline :ref:`errors` with
two additional properties as described in the json-schema below:

::

  {
     "max_version": {
      "type": "string", "pattern": "^([1-9]\d*)\.([1-9]\d*|0)$"
     },
     "min_version": {
      "type": "string", "pattern": "^([1-9]\d*)\.([1-9]\d*|0)$"
     }
  }

An example HTTP Header response:

::

  HTTP/1.1 406 Not Acceptable
  Openstack-API-Version: compute 5.3
  Vary: OpenStack-API-Version

An example errors body response:

.. literalinclude:: microversion-errors-example.json
    :language: json
