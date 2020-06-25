.. _discoverability:

API Discoverability
===================

This topic document serves to provide guidance on how to have a public REST
API expose the URIs and resources to end users in a machine-readable way.

See also the topic document on :ref:`consuming-catalog`.

See also the topic document on :doc:`consuming-catalog/version-discovery`.

.. _versioned-and-unversioned-endpoints:

Versioned and Unversioned Endpoints
-----------------------------------

Each service should have a base endpoint which is referred to as the
"Unversioned" endpoint for the service.

.. note:: It is highly recommended that Cloud Operators register the
          Unversioned Endpoint for a service in the Keystone Catalog. If they
          do, the process described in the :ref:`version-discovery-algorithm` will
          be able to be both the most featureful for the API Consumer and the
          most efficient.

Each service must have at least one Major API version.

If a service has, or expects to have, more than one Major API version,
each of those versions should have a base endpoint which is referred to
as the "Versioned" endpoint for that version of the service.

All version discovery documents must be accessible via unauthenticated
connection.

If a service only uses microversions and only has one Major API version,
that service should not have any additional "Versioned" endpoints.

For instance, the Glance service at cloud ``example.com`` might have an
Unversioned Endpoint at::

  https://image.example.com

That Glance service may then also provide three major versions, `v1`, `v2`, and
`v3`::

  https://image.example.com/v1
  https://image.example.com/v2
  https://image.example.com/v3

Additionally, the Placement service at cloud ``example.com`` might have
an Unversioned Endpoint at::

  https://placement.example.com

The Placement service only uses microversions, so there are no additional
Versioned Endpoints.

In both cases, the Unversioned Endpoint is the endpoint recommended to be
registered in the Service Catalog.

Preference for Subpaths
~~~~~~~~~~~~~~~~~~~~~~~

Historically each of the OpenStack services were also given a port. It is
strongly recommended to not use those ports and instead use the normal port
443 for https. If multiple API services are to be installed on a single
machine, it is highly recommended to use subpaths::

  https://api.example.com/compute
  https://api.example.com/image

The rationale behind this recommendation is to ease use for users who may have
restrictive port-blocking firewalls in their operating environment. Since the
traffic is HTTP traffic and not a different protocol, it is not necessary to
distinguish it by port number, and doing so increases the chances that users
will have problems connecting to individual API endpoints.

.. _version-discovery:

Version Discovery
-----------------

Each service should provide a Version Discovery API on both the Unversioned
Endpoint and each of Versioned Endpoints of the service to be used by clients
to discover the supported API versions.

.. _unversioned-version-discovery:

Unversioned Discovery
~~~~~~~~~~~~~~~~~~~~~

Each service should provide a Version Discovery API at the Unversioned Endpoint
of the service. It should be exposed to all users without authentication.

.. note:: It is recommended that the Version Discovery API not be protected
          by authentication requirements. The information returned is not
          specific to a user, but is, instead, a fundamental characteristic
          of the base API of the service running. Additionally, the v2 and
          v3 authentication API are different, so requiring authentication
          before version discovery makes it harder to determine reliably
          whether v2 or v3 authentication should be used.

The Unversioned Version Discovery API for each service should return a list of
Version Information for all of the Base Endpoints the service provides,
along with that version's minimum and maximum microversions. These values are
used by the client to discover the supported API versions.


:download:`Version Information Schema <version-information-schema.json>`

.. literalinclude:: version-information-schema.json
    :language: json

:download:`Version Discovery Schema <version-discovery-schema.json>`

.. literalinclude:: version-discovery-schema.json
    :language: json

.. _unversioned-discovery-response:

An Unversioned Version Discovery response would look as follows:

.. code-block::

    GET /

.. code-block:: json

    {
         "versions": [
              {
                  "id": "v2.1",
                  "links": [
                      {
                          "href": "https://compute.example.com/v2/",
                          "rel": "self"
                      },
                      {
                          "href": "https://compute.example.com/",
                          "rel": "collection"
                      }
                  ],
                  "status": "CURRENT",
                  "max_version": "5.2",
                  "min_version": "2.1"
              },
       ]
    }

Each Version Information in the list should contain the following information:

id
  The major API version. Follows format outlined in :ref:`versioning`,
  preceeded by a "v". Required.

links
  Contains information about where to find the actual versioned endpoint. See
  :ref:`version-links` below. Required.

status
  Support and lifecycle status of the versioned endpoint. Required.
  See :ref:`endpoint-status`

max_version
  The maximum microversion available if the version of the service supports
  microversions. Optional. See :ref:`microversion_specification`

min_version
  The minimum microversion available if the version of the service supports
  microversions. Optional. See :ref:`microversion_specification`

If a service has no Versioned Endpoints, it should simply list its Base
Endpoint in the document, like so:

.. code-block::

    GET /

.. code-block:: json

    {
         "versions": [
              {
                  "id": "v1.0",
                  "links": [
                      {
                          "href": "https://placement.example.com/",
                          "rel": "self"
                      },
                      {
                          "href": "https://placement.example.com/",
                          "rel": "collection"
                      }
                  ],
                  "status": "CURRENT",
                  "max_version": "1.25",
                  "min_version": "1.0"
              }
         ]
    }

.. _versioned-version-discovery:

Versioned Discovery
~~~~~~~~~~~~~~~~~~~

Each service should provide a Version Discovery API at each Versioned Endpoint
of the service. It should be exposed to all users without authentication.

The document returned from the Version Discovery API for Versioned Endpoint
should be identical to the document returned from the Unversioned Endpoint.
In this way, a client that is looking for a version of an API can always
get the complete information in one step, rather than a sequence of attempts,
failures and re-attempts.

However, in service of getting to a perfect future from amidst an imperfect
past, services that already deliver a different document on their Versioned
Endpoints who are concerned with API breakage resulting from changing the
payload of their Versioned Version Discovery Document from a single object
named ``version`` to a list of objects named ``versions``, it can be
nonetheless a step forward to add a link to the list of links provided
that points to the Unversioned Discovery Endpoint.

For services that do not return the Versioned Version Discovery Document
inside of an object named ``version`` but instead with the information
directly in the root object, it is similarly suggested to add the
``collection`` link. (see
https://www.iana.org/assignments/link-relations/link-relations.xhtml for
the list of defined relation types)

:download:`Versioned Discovery Schema <versioned-discovery-schema.json>`

.. literalinclude:: versioned-discovery-schema.json
    :language: json

For example:

.. code-block::

    GET /v2

.. code-block:: json

    {
         "version": {
              "id": "v2.0",
              "links": [
                  {
                      "href": "https://image.example.com/v2",
                      "rel": "self"
                  },
                  {
                      "href": "https://image.example.com/",
                      "rel": "collection"
                  }
              ],
              "status": "CURRENT"
          }
    }

.. _endpoint-status:

Endpoint Status
---------------

While it is typical for there to only be a single versioned API for a given
service, it is also sometimes useful to be able to offer more than one version
of a given API. Common examples of this are when an older version is still
made available in order to support clients that have not yet upgraded to the
current version, or when a new API version is being tested before it is
released. To distinguish these different APIs for the same service, the
`status` value is used. The following values can be returned for status:

CURRENT
  The newest API that is currently being developed and improved.
  Unless you need to support old code, use this API. One and only
  one API must be marked as CURRENT.

SUPPORTED
  An older version of the API. No new features will be added to this version,
  but any bugs discovered in the code may be fixed.

DEPRECATED
  This API will be removed in the foreseeable future. You should start
  planning on using alternatives.

EXPERIMENTAL
  This API is under development ('alpha'), and you can expect it to change or
  even be removed.

.. _version-links:

Version Links
-------------

.. note:: The ``links`` conform to the :ref:`links` guideline.

The ``links`` field of the endpoint description should contain at least
two entries, listed here by the value of their ``rel`` field.

self
  The location of the base endpoint for the given version of the service.

collection
  The location of the base endpoint for the Unversioned Version Discovery
  Endpoint. The ``collection`` entry provides guidance to allow a client to
  navigate from a Versioned Endpoint that may have been listed in the
  Service Catalog to the Unversioned Endpoint if they are looking for a
  different version without resorting to attempting to guess at URL schemes
  and performing URL manipulation.

Guidance
--------

**TODO** Add sections that describe a best practice for API discoverability,
possibly using JSON-Home, JSONSchema documents, and JSON-HAL.
