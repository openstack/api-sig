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

Versioning of the API should be single monotonic counter taking the form
X.Y following these conventions:

* X should only be changed if a significant backwards incompatible
  API change is made which affects the API as whole. That is, something
  that is only very rarely incremented. X should be changed in the following
  cases.

  * A number of endpoints get replaced by others
  * Drastic changes in API consumer workflow

* Y should be changed when you make any change to the API. Note that this
  includes semantic changes which may not affect the input or output formats or
  even originate in the API code layer. We are not distinguishing
  between backwards compatible and backwards incompatible changes in
  the versioning system. It will however be made clear in the
  documentation as to what is a backwards compatible change and what
  is a backwards incompatible one.

.. note:: Note that these versions numbers do not follow the rules of
   `Semantic Versioning <http://semver.org/>`_.

There are minimum and maximum versions which are used to describe what the
server can understand. The minimum and maximum versions are the oldest and
most recent versions supported. So clients can specify different version in
the supporting range for each API call on the same server. The minimum version
can be increased when supporting old clients is too great a burden.
Increasing the minimum version means breaking the old clients, this happens
very rarely also.

Each version includes all the changes since minimum version was introduced.
It is not possible to request the feature introduced at microversion X.Y
without accepting all the changes before X.Y in the same request.
For example, you cannot request the feature which was introduced at
microversion 2.100 without backwards incompatible changes which were
introduced in microversion 2.99 and earlier.

Client Interaction
------------------

A client specifies the version of the API they want via the following
approach, a new header::

  OpenStack-API-Version: [SERVICE_TYPE] [VERSION_STRING]

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

* The value of ``OpenStack-API-Version`` header is
  ``[SERVICE_TYPE] [VERSION_STRING]``. The VERSION_STRING must match
  `"^([1-9]\d*)\.([1-9]\d*|0)$"`. If the VERSION_STRING doesn't match the regex
  pattern, return a 400 Bad Request with an error response body that conforms
  to the errors guideline :ref:`errors`.

* If OpenStack-API-Version header is sent, the service type matches, and
  the version is set to the special keyword ``latest`` behave as if
  maximum version was specified.

.. warning:: The ``latest`` value is mostly meant for integration testing and
  would be dangerous to rely on in client code since microversions are not
  following `semver <http://semver.org/>`_ and therefore backward compatibility
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

.. note:: A Python library called `microversion-parse`_ is available
          to help with server-side processing of microversion
          headers, both the new style described in this document and
          previous forms.

.. _microversion-parse: https://pypi.org/project/microversion_parse

Version Discovery
-----------------

The Version API for each service should return the minimum and maximum
versions. These values are used by the client to discover the supported API
versions. If a service ever decides to raise the minimum version that will be
supported, it should also return the next minimum version, as well as a date
until which the current minimum version is guaranteed to be supported. If there
are no plans to change the minimum microversion, the next minimum version and
support date should be omitted.

A version response for a service that is planning on raising its minimum
supported version would look as follows::

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
                "max_version": "2.42",
                "min_version": "2.1",
                "next_min_version": "2.13",
                "not_before": "2019-12-31"
            },
       ]
    }

.. note:: The ``links`` conform to the :ref:`links` guideline.

"max_version" is the maximum version supported; "min_version" is the minimum
version supported; "next_min_version" is the planned next minimum version; and
"not_before" is the date (in ISO YYYY-MM-DD format) before which the minimum
will not change. Note that this doesn't require that the minimum be raised on
that date; that can happen any time afterwards. It is there to give operators a
sense of how quickly they need to change their tooling to support it.

If there is no planned change to the minimum version, the response can omit the
'next_min_version' and 'not_before' values. Such a response would look like::

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
                "max_version": "2.42",
                "min_version": "2.1",
            },
       ]
    }

While it is typical for there to be a single API for a given service, it is
also sometimes useful to be able to offer more than one version of a given API.
Common examples of this are when an older version is still made available in
order to support clients that have not yet upgraded to the current version, or
when a new API version is being tested before it is released. To distinguish
these different APIs for the same service, the `status` value is used. The
following values can be returned for status:

============  =======
Status        Meaning
============  =======
CURRENT       The newest API that is currently being developed and improved.
              Unless you need to support old code, use this API.
SUPPORTED     An older version of the API. No new features will be added to
              this version, but any bugs discovered in the code may be fixed.
DEPRECATED    This API will be removed in the foreseeable future. You should
              start planning on using alternatives.
EXPERIMENTAL  This API is under development ('alpha'), and you can expect it to
              change or even be removed.
============  =======

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
