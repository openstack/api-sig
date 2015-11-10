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

TBD

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
