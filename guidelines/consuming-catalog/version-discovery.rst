=================
Version Discovery
=================

The topic document on :ref:`discoverability` describes how REST services can
expose version discovery information. However, due to seven years of existence
that pre-date the existence of that document, there are a few non-optimal
setups in the wild. This document describes the complete algorithm to correctly
consume OpenStack version discovery. The intent with this algorithm is that for
all clouds that fully implement :ref:`discoverability` guidelines the path
through the system should be the most efficient, but that process degrades
gracefully for systems that do not yet... ultimately degrading all the way back
to being behaviorally the same as the "just use what's in the catalog" method.

.. note:: This document contains references to dealing with all known forms
          of things encountered in the wild. Where it doesn't distract from the
          rest of the description, care is taken to indicate which form is the
          preferred form and which are supported for legacy reasons.
          Mention of a form in this document should not be construed as
          endorsement. Definitions of preferred forms of data will be found
          in other documents.

.. _version-discovery-algorithm:

Version Discovery Algorithm
===========================

The Version Discovery Algorithm is a part of :doc:`../consuming-catalog`. Its
input parameters and return values are a subset of the input parameters and
return values described in :ref:`catalog-user-request`. It is expeced at this
point that the ``{catalog-endpoint}`` is already known, either from the Service
Catalog or directly from ``{endpoint-override}``.

The algorithm is as follows:

#. If the user has omitted ``{endpoint-version}``, follow
   `User Omitted API Version`_.

#. Infer the ``{found-endpoint-version}`` from the ``{catalog-endpoint}`` using
   the `Inferring Version`_ process.

#. If ``{found-endpoint-version}`` exists and ``{fetch-version-information}``
   is false, STOP. Return ``{catalog-endpoint}`` as ``{service-endpoint}``.

#. If the `Inferring Version`_ process returned an error, the
   ``{catalog-endpoint}`` does not match the ``{endpoint-version}``. Attempt to
   `Find a Document`_.

   .. note:: If the :ref:`discoverability` guidelines have been implemented,
             there will always be a ``{discovery-document}``.

#. If it is not possible to find a ``{discovery-document}`` and ``{be-strict}``
   is true, STOP. Return an error that version discovery has failed.

#. Determine ``{single-or-multiple}`` for the ``{discovery-document}``
   (see `Single or Multiple Version Documents`_).

   .. note:: If the :ref:`discoverability` guidelines have been implemented,
             ``{single-or-multiple}`` will always be ``multiple``.

At this point, there is a matrix of four possibilities:

#. If ``{endpoint-version}`` is ``latest`` and ``{single-or-multiple}`` is
   ``single``, follow `Latest Single Version`_.

#. If ``{endpoint-version}`` is ``latest`` and ``{single-or-multiple}`` is
   ``multiple``, follow `Latest Multiple Versions`_.

#. If ``{endpoint-version}`` is a version and ``{single-or-multiple}`` is
   ``single``, follow `Requested Single Version`_.

#. If ``{endpoint-version}`` is a version and ``{single-or-multiple}`` is
   ``multiple``, follow `Requested Multiple Versions`_.

User Omitted API Version
------------------------

If the user has omitted the API Version, then the user is indicating that they
want to use the ``{catalog-endpoint}`` as their ``{service-endpoint}``.
Discovery is only run to find out version information about that endpoint.

#. ``{service-endpoint}`` is ``{catalog-endpoint}``.

#. If ``{fetch-version-information}`` is false, STOP. Infer the
   ``{found-endpoint-version}`` from ``{service-endpoint}``.
   (see `Inferring Version`_)

#. Retrieve ``{discovery-document}`` at ``{service-endpoint}``.

#. If a ``{discovery-document}`` is found, STOP. Return the
   ``{endpoint-information}`` in it (see `Return Information`_).

#. If there is no ``{discovery-document}``, attempt to `Find a Document`_.

#. If there is no ``{discovery-document}``, STOP Infer the
   ``{found-endpoint-version}`` from ``{service-endpoint}``.
   (see `Inferring Version`_)

#. Determine if the ``{single-or-multiple}`` of the ``{discovery-document}`` is
   ``single`` or ``multiple`` (see `Single or Multiple Version Documents`_).

#. If ``{single-or-multiple}`` is ``single``, STOP. Return the
   ``{endpoint-information}`` in it (see `Return Information`_).

#. If ``{single-or-multiple}`` is ``multiple``, find the
   ``{endpoint-information}`` in the ``{discovery-document}`` that matches
   ``{service-endpoint}`` (see `Matching Endpoints`_).

#. If there is no ``{endpoint-information}``, STOP. Infer the
   ``{found-endpoint-version}`` from ``{catalog-endpoint}``.
   (see `Inferring Version`_)

#. STOP. Return the information in ``{endpoint-information}`` (see
   `Return Information`_).

Find a Document
---------------

In some cases, the ``{discovery-endpoint}`` will either not return a document,
or will not return the document we want, so we need to look for a new one.

The Unversioned Document is always preferred over the Versioned Document,
because the Unversioned Document supplies the list of possible versions,
allowing Discovery to process the list and make decisions in one step. The
Versioned Document only contains one Version, so additional calls must be
made if the version in it does not match the user's request.

The algorithm for finding a new document is as follows:

#. If there is an existing ``{discovery-document}`` and
   ``{single-or-multiple}`` is ``multiple``, STOP. There is no better document.

#. If

   * there is an existing ``{discovery-document}``
   * ``{single-or-multiple}`` is ``single``
   * the ``collection`` link in the links section is different than the
     current ``{discovery-endpoint}``

   make the endpoint at the ``collection`` link the new
   ``{discovery-endpoint}`` and fetch a new ``{discovery-document}``. STOP.
   Return the new ``{discovery-document}``.

#. Get the curently scoped ``project_id`` from the ``token``, if one exists.

#. If the ``{discovery-endpoint}`` ends with a path element that ends with
   the ``project_id``, remove that path element and make the resulting URL
   the new ``{discovery-endpoint}``.

#. If the current ``{discovery-endpoint}`` ends with a path element that ends
   with a version string of the form "v[0-9]+(\.[0-9]+)?$", remove that path
   element but save it as ``{removed-version-path-element}``. Make the
   resulting URL the new ``{discovery-endpoint}``.

#. If the ``{discovery-endpoint}`` matches the ``{catalog-endpoint}``, STOP.
   Return an error reporting no working ``{discovery-document}``.

#. Attempt to fetch a ``{discovery-document}`` from the
   ``{discovery-endpoint}``. If one exists, STOP. Normalize it (see
   `Normalizing Documents`_) and return it as the ``{dicovery-document}``.

#. If no new ``{discovery-document}`` can be found at the new endpoint but
   there is a saved value in ``{removed-version-path-element}``, append
   the ``{removed-version-path-element}`` to the ``{discovery-endpoint}`` and
   make the resulting URL the new ``{discovery-endpoint}``.

#. Attempt to fetch a ``{discovery-document}`` from the
   ``{discovery-endpoint}``. If one exists, STOP. Normalize it (see
   `Normalizing Documents`_) and return it as the ``{dicovery-document}``.

#. If no document can be found, return an error reporting no working
   ``{discovery-document}``.

For example:

.. code-block:: python

  # Given a discovery document from the cloud
  original_document = {
    "version": {
      "status": "SUPPORTED",
      "id": "v2.0",
      "links": [
        {
          "href": "http://compute.example.com/v2/",
          "rel": "self"
        },
        {
          "href": "http://compute.example.com/",
          "rel": "collection"
        }
      ]
    }
  }

  # It is a single version document
  single_or_multiple = 'single'

  # We apply the normalization process
  normalized_document = {
    "versions": [
      {
        "status": "SUPPORTED",
        "id": "v2.0",
        "min_version": "",
        "max_version": "",
        "links": [
          {
            "href": "http://compute.example.com/v2/",
            "rel": "self"
          },
          {
            "href": "http://compute.example.com/",
            "rel": "collection"
          }
        ]
      }
    ]
  }

  # We see that a collection link exists, so we'll use it as the new discovery
  # endpoint.
  discovery_endpoint = "http://compute.example.com/"

  # We fetch the document from that endpoint and normalize it.
  normalized_better_discovery_document = {
    "versions": [
      {
        "status": "SUPPORTED",
        "links": [
          {
            "href": "http://compute.example.com/v2/",
            "rel": "self"
          }
        ],
        "min_version": "",
        "max_version": "",
        "id": "v2.0"
      }, {
        "status": "CURRENT",
        "links": [
          {
            "href": "http://compute.example.com/v2.1/",
            "rel": "self"
          }
        ],
        "min_version": "2.1",
        "max_version": "2.38",
        "id": "v2.1"
      }
    ]
  }

  # single-or-multiple is multiple, so it's better
  return normalized_better_discovery_document

Example with project_id:

.. code-block:: python

  # The user has requested service-type=file-storage

  # The user's token reports the project_id
  project_id = '45f0034e8c5a4ef4895b5a87b6b57def'
  # The service-catalog contains an entry for filestorage
  catalog_endpoint = 'https://file-storage.example.com/v2/45f0034e8c5a4ef4895b5a87b6b57def'

  # The catalog_endpoint ends with the user's project_id, so we pop it.
  new_endpoint = 'https://file-storage.example.com/v2'

  # Fetch the document, normalize it and return it
  return {
    "versions": [
      {
        "status": "CURRENT",
        "id": "v2.0",
        "links": [
          {
            "href": "http://file-storage.example.com/v2/",
            "rel": "self"
          },
          {
            "href": "http://file-storage.example.com/",
            "rel": "collection"
          }
        ]
      }
    ]
  }

More pathological example:

.. code-block:: python

  # The user has requested service-type=file-storage

  # The user's token reports the project_id
  project_id = '45f0034e8c5a4ef4895b5a87b6b57def'
  catalog_endpoint = 'https://file-storage.example.com/v2/45f0034e8c5a4ef4895b5a87b6b57def'

  # The catalog_endpoint ends with the user's project_id, so we pop it.
  discovery_endpoint = 'https://file-storage.example.com/v2'

  # We try to fetch https://file-storage.example.com/v2 but it returns an error

  # Pop version string from the endpoint
  new_discovery_endpoint = 'https://file-storage.example.com/'

  # Fetch the document, normalize and return it
  return {
    "versions": [
      {
        "status": "SUPPORTED",
        "links": [
          {
            "href": "http://file-storage.example.com/v1/",
            "rel": "self"
          }
        ],
        "min_version": "",
        "max_version": "",
        "id": "v1.0"
      },
      {
        "status": "CURRENT",
        "links": [
          {
            "href": "http://file-storage.example.com/v2/",
            "rel": "self"
          }
        ],
        "min_version": "2.0",
        "max_version": "2.22",
        "id": "v2.0"
      }
    ]
  }

Inferring Version
-----------------

In most cases the version of the ``{service-endpoint}`` should be retrievable
from the ``{discovery-document}``, and in those cases it should be considered
the version of the service at the ``{service-endpoint}``. In some cases no
discovery document can be found corresponding with the ``{service-endpoint}``
in question. Alternately, in some cases the ``{catalog-endpoint}`` contains
version information and the user is not looking for microversion information.

Microversion information will always be empty when this procedure is used.

The algorithm for inferring the version is as follows:

#. Get the curently scoped ``project_id`` from the token, if one exists.

#. If the endpoint ends with a path element that ends with ``project_id``,
   remove it.

#. If the endpoint ends with a path element that is of the form,
   ``^v[0-9]+(\.[0-9]+)?$``, strip the ``v`` and use the rest of that element
   as ``{found-endpoint-version}``.

#. If the endpoint contains no version elements, a version cannot be inferred.
   Return a null value for ``{found-endpoint-version}``.

#. If ``{endpoint-version}`` was given and does not match
   ``{found-endpoint-version}``, STOP. Return an error that says that user
   requested a version and that the version inferred from the URL did not
   match.

#. Return ``{found-endpoint-version}``.

For example:

.. code-block:: python

  catalog_endpoint = 'https://file-storage.example.com/v2/45f0034e8c5a4ef4895b5a87b6b57def'
  # Match path elements - /v2/ matches ...
  found_api_version = '2'

  catalog_endpoint = 'https://identity-storage.example.com/'
  # Match path elements - no matches
  found_api_version = None

  catalog_endpoint = 'https://object-store.example.com/v1/AUTH_622b11a1-5dfa-43b4-9f58-4ad3c6dbc4a0'
  # Match path elements - /v1/ matches ...
  found_api_version = '1'

  catalog_endpoint = 'https://compute.example.com/v2.1'
  # Match path elements - /v2.1/ matches ...
  found_api_version = '2.1'

Matching Endpoints
------------------

If ``{single-or-multiple}`` is ``multiple`` and the discovery algorithm has
chosen to fall back to the endpoint provided by the catalog, a URL matching the
catalog URL should be found so that the version can be extracted.

#. Sort the endpoints in the ``{discovery-document}`` by ``id`` in descending
   order using version comparision.

#. For each endpoint in the list, expand it (see `Expanding Endpoints`_)
   and compare it to the catalog endpoint. The first endpoint that matches is
   the winner.

For example:

.. code-block:: python

  catalog_endpoint = 'https://file-storage.example.com/v2/45f0034e8c5a4ef4895b5a87b6b57def'

  discovery_document = {
    "versions": [
      {
        "status": "CURRENT",
        "id": "v2.0",
        "links": [
          {
            "href": "http://file-storage.example.com/v2/",
            "rel": "self"
          }
        ],
      }
    ]
  }

  # Expand endpoint http://file-storage.example.com/v2/
  expanded_endpoint = "https://file-storage.example.com/v2/45f0034e8c5a4ef4895b5a87b6b57def"

  # expanded_endpoint matches catalog_endpoint - id v2.0 is the match

Expanding Endpoints
-------------------

Endpoints in discovery documents can be relative and can also be erroneous in
known ways. Before using endpoints from discovery documents, they must be
expanded. The algorithm is as follows:

#. Join the endpoint from the discovery document with the endpoint the
   discovery document was fetched from. If the endpoint in the document is
   an absolute url, this should result in the endpoint from the document being
   unchanged. If the endpoint from the document is relative, it should be
   be appended to the endpoint the document was fetched from following normal
   relative URL rules. The python module ``six.moves.urllib.parse.urljoin`` is
   an example of an implementation of url joining that behaves as expected.

#. Replace the ``scheme`` and ``host`` of the endpoint from the discovery
   document with the ``scheme`` and ``host`` from the endpoint it was fetched
   from. This is to work around older buggy discovery documents seen in the
   wild.

   For example:

.. code-block:: python

   def replace_scheme(endpoint, discovery_url):
        parsed_endpoint = urllib.parse.urlparse(endpoint)
        parsed_discovery_url = urllib.parse.urlparse(discovery_url)

        return urllib.parse.ParseResult(
            parsed_discovery_url.scheme,
            parsed_discovery_url.netloc,
            parsed_endpoint.path,
            parsed_endpoint.params,
            parsed_endpoint.query,
            parsed_endpoint.fragment).geturl()

#. Get the curently scoped ``project_id`` from the token, if one exists.

#. If the ``{catalog-endpoint}`` ends with a path element that ends with
   ``project_id`` but the endpoint does not, append the final element of the
   path of the ``{catalog-endpoint}`` to the end of the endpoint.

.. note:: Some services prepend a string to the project_id in their endpoint,
          so just appending the project_id to the catalog-endpoint is not
          sufficient.

For example:

.. code-block:: python

  project_id = '45f0034e8c5a4ef4895b5a87b6b57def'
  catalog_endpoint = 'https://file-storage.example.com/v2/45f0034e8c5a4ef4895b5a87b6b57def'

  discovery_document = {
    "versions": [
      {
        "status": "CURRENT",
        "id": "v2.0",
        "links": [
          {
            "href": "/v2.0",
            "rel": "self"
          }
        ]
      }
    ]
  }

  # Pop project_id from catalog_endpoint
  shortened_catalog_endpoint = 'https://file-storage.example.com/v2'

  # Apply URL join to https://file-storage.example.com/v2 and /v2.0
  joined_endpoint = 'https://file-storage.example.com/v2.0'

  # catalog_endpoint ends with project_id, append project_id
  service_endpoint = 'http://file-storage.example.com/v2.0/45f0034e8c5a4ef4895b5a87b6b57def'

With broken service endpoint in discovery:

.. code-block:: python

  project_id = '45f0034e8c5a4ef4895b5a87b6b57def'
  catalog_endpoint = 'https://file-storage.example.com/v2/45f0034e8c5a4ef4895b5a87b6b57def'

  # This discovery_document is the result of a service with a broken
  # configuration. Obviously the service is not on "localhost". Similarly,
  # since the discovery endpoint is an https endpoint, it can be assumed
  # that the actual service endpoint is https.
  discovery_document = {
    "versions": [
      {
        "status": "CURRENT",
        "id": "v2.0",
        "links": [
          {
            "href": "http://localhost/v2.0",
            "rel": "self"
          }
        ],
      }
    ]
  }

  # Pop project_id from catalog_endpoint
  shortened_catalog_endpoint = 'https://file-storage.example.com/v2'

  # Apply URL join to https://file-storage.example.com/v2 and
  # http://localhost/v2.0 - endpoint from discovery is absolute
  joined_endpoint = 'http://localhost/v2.0'

  # Replace scheme and host from https://file-storage.example.com/v2
  joined_endpoint = 'https://file-storage.example.com/v2.0'

  # catalog_endpoint ends with project_id, append project_id
  service_endpoint = 'http://file-storage.example.com/v2.0/45f0034e8c5a4ef4895b5a87b6b57def'

Single or Multiple Version Documents
------------------------------------

Even with the version documents normalized as per `Normalizing Documents`_
into the form described by :ref:`discoverability`, it is still
important to know if the document lists all available versions or only a
single out of a larger set. As it's also possible that there is only one
version, merely looking at the length of the list is not sufficient.

.. note:: Once all services implement the full recommendations in
          :ref:`discoverability` there will never be a document
          with a single version out of a larger set, so this logic will not
          be needed. However, the logic is upwards compatible with that
          desired future state.

In order to apply the discovery algorithm, the type of document must be
detected.

* If the document has a link description in the ``links`` list with a ``rel``
  of ``collection`` and the ``href`` of that link is different than the
  ``href`` of the link with a ``rel`` of ``self``, then it is a Single
  Version Document.

* Otherwise it is a Multiple Version Document and can be relied on to contain
  the complete set of available versions.

.. note:: TODO(mordred) add examples

Normalizing Documents
---------------------

.. note:: If the API-SIG recommendations in :ref:`discoverability`
          are implemented, all of the logic in this section can be skipped.

There are three forms of existing version discovery documents in addition to
the one that is preferred and described in :ref:`discoverability`.
In order to apply the algorithm sanely, the fetched documents should be
normalized to align with the :ref:`discoverability`.

.. note:: It is not actually required that normalization take place in a
          client or library. It is described here for the purposes of
          simplifying other parts of this document and being able to describe
          the process in terms of the correct document formats.

* If the document has a key named ``versions`` which contains a dict with a
  key named ``values``, move the list contained in ``values`` to be directly
  under ``versions``. That list is then the list of Version objects.

For example:

.. code-block:: json

  {
    "versions": {
      "values": [
        {
          "status": "stable",
          "updated": "2016-10-06T00:00:00Z",
          "id": "v3.7",
          "links": [
            {
              "href": "https://auth.example.com/v3/",
              "rel": "self"
            }
          ]
        },
        {
          "status": "deprecated",
          "updated": "2016-08-04T00:00:00Z",
          "id": "v2.0",
          "links": [
            {
              "href": "https://auth.example.com/v2.0/",
              "rel": "self"
            }
          ]
        }
      ]
    }
  }

becomes:

.. code-block:: json

  {
    "versions": [
      {
        "status": "stable",
        "updated": "2016-10-06T00:00:00Z",
        "id": "v3.7",
        "links": [
          {
            "href": "https://auth.example.com/v3/",
            "rel": "self"
          }
        ]
      },
      {
        "status": "deprecated",
        "updated": "2016-08-04T00:00:00Z",
        "id": "v2.0",
        "links": [
          {
            "href": "https://auth.example.com/v2.0/",
            "rel": "self"
          }
        ]
      }
    ]
  }

* If the document has a key named ``id`` make a key named ``version`` and
  place all of the values under it.

For example:

.. code-block:: json

  {
    "status": "CURRENT",
    "id": "v2.0",
    "links": [
      {
        "href": "http://network.example.com/v2.0",
        "rel": "self"
      }
    ]
  }

becomes:

.. code-block:: json

  {
    "version": {
      "status": "CURRENT",
      "id": "v2.0",
      "links": [
        {
          "href": "http://network.example.com/v2.0",
          "rel": "self"
        }
      ]
    }
  }

* If the document has a key named ``version``, (even if you just created it)
  look for a ``collection`` link in the links list. If one does not exist,
  grab the ``href`` from the ``self`` link. If the ``self`` link ends with a
  version string of the form "v[0-9]+(\.[0-9]+)?$", pop that version string
  from the end of the endpoint and add a ``collection`` entry to the ``links``
  list with the resulting endpoint.

For example:

.. code-block:: json

  {
    "version": {
      "status": "CURRENT",
      "id": "v2.0",
      "links": [
        {
          "href": "http://network.example.com/v2.0",
          "rel": "self"
        }
      ]
    }
  }

becomes:

.. code-block:: json

  {
    "version": {
      "status": "CURRENT",
      "id": "v2.0",
      "links": [
        {
          "href": "http://network.example.com/v2.0",
          "rel": "self"
        },
        {
          "href": "http://network.example.com/",
          "rel": "collection"
        }
      ]
    }
  }

* If the document has a key named ``version``, create a top level key called
  ``versions`` that contains a list. Move the contents of ``version`` into
  a dict in the ``versions`` list and remove the top level key ``version``.

For example:

.. code-block:: json

  {
    "version": {
      "status": "CURRENT",
      "id": "v2.0",
      "links": [
        {
          "href": "http://network.example.com/v2.0",
          "rel": "self"
        },
        {
          "href": "http://network.example.com/",
          "rel": "collection"
        }
      ]
    }
  }

becomes:

.. code-block:: json

  {
    "versions": [
      {
        "status": "CURRENT",
        "id": "v2.0",
        "links": [
          {
            "href": "http://network.example.com/v2.0",
            "rel": "self"
          },
          {
            "href": "http://network.example.com/",
            "rel": "collection"
          }
        ]
      }
    ]
  }

For each Version object in the ``versions`` list:

#. Keys other than ``id``, ``version``, ``min_version``, ``max_version``,
   ``status`` and ``links`` can be ignored or removed.

#. Convert the value in the ``status`` field to upper case.

#. If ``status`` is ``STABLE``, change it to ``CURRENT``. (handles keystone)

#. If there is a ``version`` field and not a ``max_version`` field, make a
   ``max_version`` field with the value from the ``version`` field. (handles
   nova, cinder, manila and ironic microversions)

#. The ``links`` key should contain a list, and that list should contain one
   dict with ``rel`` equal to ``self`` and additionally may contain a second
   dict with ``rel`` equal to ``collection``. Any other entries can be
   discarded.

Some examples of the total normalization follow.

Original document:

.. code-block:: json

  {
    "versions": [
      {
        "status": "stable",
        "updated": "2016-10-06T00:00:00Z",
        "id": "v3.7",
        "links": [
          {
            "href": "https://auth.example.com/v3/",
            "rel": "self"
          }
        ]
      },
      {
        "status": "deprecated",
        "updated": "2016-08-04T00:00:00Z",
        "id": "v2.0",
        "links": [
          {
            "href": "https://auth.example.com/v2.0/",
            "rel": "self"
          }
        ]
      }
    ]
  }

becomes:

.. code-block:: json

  {
    "versions": [
      {
        "status": "CURRENT",
        "id": "v3.7",
        "links": [
          {
            "href": "https://auth.example.com/v3/",
            "rel": "self"
          }
        ]
      },
      {
        "status": "DEPRECATED",
        "id": "v2.0",
        "links": [
          {
            "href": "https://auth.example.com/v2.0/",
            "rel": "self"
          }
        ]
      }
    ]
  }

Original document:

.. code-block:: json

  {
    "versions": [
      {
        "status": "SUPPORTED",
        "updated": "2011-01-21T11:33:21Z",
        "links": [
          {
            "href": "http://compute.example.com/v2/",
            "rel": "self"
          }
        ],
        "min_version": "",
        "version": "",
        "id": "v2.0"
      },
      {
        "status": "CURRENT",
        "updated": "2013-07-23T11:33:21Z",
        "links": [
          {
            "href": "http://compute.example.com/v2.1/",
            "rel": "self"
          }
        ],
        "min_version": "2.1",
        "version": "2.38",
        "id": "v2.1"
      }
    ]
  }

becomes:

.. code-block:: json

  {
    "versions": [
      {
        "status": "SUPPORTED",
        "links": [
          {
            "href": "http://compute.example.com/v2/",
            "rel": "self"
          }
        ],
        "min_version": "",
        "max_version": "",
        "id": "v2.0"
      },
      {
        "status": "CURRENT",
        "links": [
          {
            "href": "http://compute.example.com/v2.1/",
            "rel": "self"
          }
        ],
        "min_version": "2.1",
        "max_version": "2.38",
        "id": "v2.1"
      }
    ]
  }

Find Matching Version
=====================

Finding a version out of a list of endpoint descriptions is done by comparing
``{endpoint-version}`` with the ``id`` field of the description to find a list
of ``{candidate-endpoints}`` (see :ref:`comparing-major-versions`).

If there is more than one ``{id}`` that matches the requested
``{endpoint-version}`` and one of them has ``status`` of ``CURRENT``, it should
be returned.

If there is more than one ``{id}`` that matches the requested
``{endpoint-version}`` and none has the ``status`` of ``CURRENT``, the highest
should be returned.

If there is more than one ``{id}`` that matches the requested
``{endpoint-version}`` and more than one has the ``status`` of ``CURRENT``, the
highest should be returned.

Latest Single Version
---------------------

``{endpoint-version}`` is ``latest`` and ``{single-or-multiple}`` is
``single``.

#. If ``status`` in the ``{discovery-document}`` is ``CURRENT``, STOP.
   Return the ``{endpoint-information}`` in the ``{discovery-document}``
   (see `Return Information`_).

#. Attempt to `Find a Document`_

#. If there is a new ``{discovery-document}`` determine if the
   ``{single-or-multiple}`` is ``single`` or ``multiple``
   (see `Single or Multiple Version Documents`_).

#. If new ``{single-or-multiple}`` is ``multiple``, follow
   `Latest Multiple Versions`_.

#. If new ``{single-or-multiple}`` is ``single``, or there is no new
   ``{discovery-document}``, STOP. Return the ``{endpoint-information}`` in
   the ``{discovery-document}`` (see `Return Information`_).

Latest Multiple Versions
------------------------

``{endpoint-version}`` is ``latest`` and ``{single-or-multiple}`` is
``multiple``.

#. Find the ``{endpoint-information}`` in the ``{discovery-document}``
   with the latest version, see `Find Latest Version`_.

#. When ``{endpoint-information}`` is found, STOP. Return the information in
   the ``{endpoint-information}`` (see `Return Information`_).

Requested Single Version
------------------------

``{endpoint-version}`` is a version or range and ``{single-or-multiple}`` is
``single``.

#. Check to see if the version in the ``{discovery-document}`` matches the
   ``{endpoint-version}`` by following `Find Matching Version`_.

#. Find a matching ``{endpoint-information}`` in the ``{discovery-document}``
   that matches the ``{endpoint-version}``. (see `Find Matching Version`_)

#. If ``{endpoint-information}`` is found, STOP. Return the information in the
   ``{endpoint-information}`` (see `Return Information`_).

#. If the version does not match, attempt to `Find a Document`_.

#. If there is a new ``{discovery-document}`` determine if the
   ``{single-or-multiple}`` is ``single`` or ``multiple``
   (see `Single or Multiple Version Documents`_).

#. If the ``{single-or-multiple}`` is ``multiple``, follow
   `Requested Multiple Versions`_.

#. If there is no new ``{discovery-document}``, STOP. Return an error telling
   the user their requested version could not be found. Include the version
   that was found in the error.

Requested Multiple Versions
---------------------------

``{endpoint-version}`` is a version or range and ``{single-or-multiple}`` is
``multiple``.

#. Find a matching ``{endpoint-information}`` in the ``{discovery-document}``
   (see `Find Matching Version`_)

#. If ``{endpoint-information}`` is found, STOP. Return the information in the
   ``{endpoint-information}`` (see `Return Information`_).

#. If no matching ``{endpoint-information}`` is found and
   ``{be-strict}`` is ``True``, STOP. Return an error telling the
   user their requested version could not be found. Include the list of
   versions that were found in the error.

#. If no matching ``{endpoint-information}`` is found and
   ``{be-strict}`` is False, use the ``{catalog-endpoint}`` as the
   ``{service-endpoint}``. Find the ``{endpoint-information}``
   in the document that matches the ``{catalog-endpoint}`` and use it.
   (see `Matching Endpoints`_).

#. If there is no ``{endpoint-information}``, STOP. Infer the
   ``{found-endpoint-version}`` from the ``{service-endpoint}``
   (see `Inferring Version`_).

#. STOP. Return the information in ``{endpoint-information}`` (see
   `Return Information`_).

Find Latest Version
-------------------

If one of the versions in the list has ``status`` of ``CURRENT``, use it.

Otherwise, select the version with the highest ``id``, excluding any with
``status`` of ``EXPERIMENTAL`` or ``DEPRECATED`` sorted using version
comparison not lexical sorting.

Return Information
==================

When endpoint information has been selected, return the information in the
following manner:

#. Strip the leading "v" from ``{id}`` and return it as
   ``{found-endpoint-version}``.

#. Expand the ``href`` of the entry in ``links`` where ``rel`` is ``self``
   and return it as the ``{service-endpoint}`` (see `Expanding Endpoints`_).

#. Return ``{min-version}`` and ``{max-version}`` if they exist.
