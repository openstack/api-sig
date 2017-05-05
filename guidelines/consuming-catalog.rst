.. _consuming-catalog:

=========================
Consuming Service Catalog
=========================

This document describes the process to correctly find a service's endpoint
from the Service Catalog.

.. note:: The process described in this document is compatible with all known
          OpenStack Public Clouds and also matches the behavior of the python
          library keystoneauth, which is the reference implementation of
          authenticating with keystone and consuming information from the
          catalog. In some places an argument can be made for a different
          process, but given keystoneauth's wide use and reference nature,
          we've chosen to keep backwards compatibility with keystoneauth's
          behavior rather than design a new perfect process. keystoneauth
          itself notes internally places where it kept backwards compatibility
          with the libraries that predate it. Notes have been left about
          stricter behavior a library or framework could choose to impose.

.. note:: The use of the word "object" in this document refers to a JSON
          object, not an Object from any particular programming language.

User Request
============

The ultimate goal of this process is for a user to find the information about
an endpoint for a service given some inputs. The user will start the process
knowing some number of these parameters. Each additional input expected from
the user without an answer of "where do they learn this information" will
increase the difficulty of a user consuming services, so client libraries and
utilities are strongly encouraged to do whatever they can to be extra helpful
in helping the user ask the right question.

.. note:: Be liberal with what you accept and strict with what you emit.

There is one piece of information that is absolutely required that the
user know:

service-type
  The generic name of the service, such as `compute` or `network`.

The user may also wish to express an alteration to the general algorithm:

be-strict
  Forgo leniant backwards compatibility concessions and be more strict in
  input and output validation.

There are several optional pieces of information that the user might know,
or additional constraints the user might wish to express.

region-name
  The region of the service the user desires to work with. May be optional,
  depending on whether the cloud has more than one region. Services
  all exist within regions, but some clouds only have one region.
  If ``{be-strict}`` has been given, ``{region-name}`` is required.

.. note:: It is highly recommended that ``{region-name}`` always be required
          to protect against single-region clouds adding a region in the
          future. However, keystoneauth today allows region-name to be omitted
          and there are a large number of clouds in existence with a single
          region named ``RegionOne``. For completely new libraries or major
          versions where breaking behavior is acceptable, requiring region-name
          by default would be preferred.

interface
  Which API interface, such as ``public``, ``internal`` or ``admin`` that
  the user wants to use. A user can also request a list of interfaces they find
  acceptable in the order of their preference, such as
  ``['internal', 'public']`` (Optional, defaults to ``public``)

service-name
  Arbitrary name given to the service by the deployer. Optional.

.. note:: In all except the most extreme cases this should never be needed and
          its use as a meaningful identifier by Deployers is strongly
          discouraged. However, the Consumer has no way to otherwise mitigate
          the situation if their Deployer has provided them with a catalog
          where a ``service-name`` must be used, so ``service-name`` must be
          accepted as input. If ``{be-strict}`` has been requested, a user
          supplying ``{service-name}`` should be an error.

service-id
  Unique identifier for an endpoint in the catalog. Optional.

.. note:: On clouds with well-formed catalogs ``service-id`` should never be
          needed. If ``{be-strict}`` has been requested, a user supplying
          ``{service-id}`` should be an error.

endpoint-override
  An endpoint for the service that the user has procurred from some other
  source. (Optional, defaults to omitted)

At the end of the discovery process, the user should know the
``{service-endpoint}``, which is the endpoint to use as the root of the
service, and the ``{interface}`` of the endpoint that was found.

In the description that follows, each of the above inputs and outputs will
be referred to like ``{endpoint-override}`` so that it is clear whether a user
supplied input to the process or one of the expected outputs is being
discussed. Other values that are fetched at one point in the process and
referred to at a later point are similarly referred to like
``{service-catalog}``. Names will not be reused within the process to
hold different content at different times.

It is also assumed that the user has an ``{auth-url}`` and authentication
information. The authentication process itself is out of the scope of this
document.

Discovery Algorithm
===================

The basic process is:

#. If the user has provided ``{endpoint-override}``, STOP. This is the
   ``{service-endpoint}``.

#. Authenticate to keystone at the ``{auth-url}``, retreiving a ``token``
   which contains the ``{service-catalog}``.

#. Retrieve ``{catalog-endpoint}`` from the ``{service-catalog}`` given
   some combination of ``{service-type}``, ``{interface}``, ``{service-name}``,
   ``{region-name}`` and ``{service-id}``. (see :ref:`endpoint-from-catalog`)

.. _endpoint-from-catalog:

Endpoint from Catalog
=====================

The ``{service-catalog}`` can be found in the ``token`` returned from
keystone authentication.

If v3 auth is used, the catalog will be in the ``catalog`` property of the
top-level ``token`` object. Such as:

.. code-block:: json

  {
    'token': {
      'catalog': {}
    }
  }

If v2 auth is used it will be in the ``serviceCatalog`` property of the
top-level ``access`` object. Such as:

.. code-block:: json

  {
    'access': {
      'serviceCatalog': {}
    }
  }

In both cases, the catalog content itself is a list of objects. Each object has
two main keys that concern discovery:

type
  Matches ``{service-type}``

endpoints
  List of endpoint objects for that service

Additionally, for backwards compatibility reasons, the following keys may
need to be checked.

name
  Matches ``{service-name}``

id
  Matches ``{service-id}``

The list of endpoints has a different format depending on whether v2 or v3 auth
was used. For both versions each endpoint object has a ``region`` key,
which should match ``{region-name}`` if one was given.

In v2 auth the endpoint object has three keys ``publicURL``,
``internalURL``, ``adminURL``. The endpoint for the ``{interface}`` requested
by the user is found in the key with the name matching ``{interface}`` plus
the string ``URL``.

In v3 auth the endpoint object has a ``url`` that is the endpoint that is
being requested if the value of ``interface`` matches ``{interface}``.

Concrete examples of tokens with catalogs:

V3 Catalog Objects:

.. code-block:: json

  {
    "token": {
      "catalog": [
          {
              "endpoints": [
                  {
                      "id": "39dc322ce86c4111b4f06c2eeae0841b",
                      "interface": "public",
                      "region": "RegionOne",
                      "url": "https://identity.example.com"
                  },
                  {
                      "id": "ec642f27474842e78bf059f6c48f4e99",
                      "interface": "internal",
                      "region": "RegionOne",
                      "url": "https://identity.example.com"
                  },
                  {
                      "id": "c609fc430175452290b62a4242e8a7e8",
                      "interface": "admin",
                      "region": "RegionOne",
                      "url": "https://identity.example.com"
                  }
              ],
              "id": "4363ae44bdf34a3981fde3b823cb9aa2",
              "type": "identity",
              "name": "keystone"
          }
      ],
  }

V2 Catalog Objects:

.. code-block:: json

  {
    "access": {
      "serviceCatalog": [
        {
          "endpoints_links": [],
          "endpoints": [
            {
              "adminURL": "https://identity.example.com/v2.0",
              "region": "RegionOne",
              "publicURL": "https://identity.example.com/v2.0",
              "internalURL": "https://identity.example.com/v2.0",
              "id": "4deb4d0504a044a395d4480741ba628c"
            }
          ],
          "type": "identity",
          "name": "keystone"
        },
      ]
    }
  }

The algorithm is:

#. Find the objects in the ``{service-catalog}`` where ``type`` matches
   ``{service-type}``.

#. If ``{service-name}`` was given and the objects remaining have a ``name``
   field, keep only the ones where ``name`` matches ``{service-name}``.

.. note:: Catalogs from Keystone v3 before v3.3 do not have a name field. If
          ``{be-strict}`` was not requested and the catalog does not have a
          ``name`` field, ``{service-name}`` should be ignored.

#. If ``{service-id}`` was given and the objects remaining have a ``id``
   field, keep only the ones where ``id`` matches ``{service-id}``.

.. note:: Catalogs from Keystone v2 do not have an id field. If
          ``{be-strict}`` was not requested and the catalog does not have a
          ``id`` field, ``{service-id}`` should be ignored.

The list of remaining objects are the ``{candidate-catalog-objects}``. If there
are no endpoints, return an error that there are no endpoints matching
``{service-type}`` and ``{service-name}``.

Use ``{candidate-catalog-objects}`` to produce the list of
``{candidate-endpoints}``.

For each endpoint object in each of the ``{candidate-catalog-objects}``:

#. If v2, if there is no key of the form ``{interface}URL`` for any of the
   the ``{interface}`` values given, discard the endpoint.

#. If v3, if ``interface`` does not match any of the ``{interface}`` values
   given, discard the endpoint.

If there are no endpoints left, return an error that there are no endpoints
matching any of the ``{interface}`` values, preferrably including the list of
interfaces that were found.

For each remaining endpoint in ``{candidate-endpoints}``:

#. If ``{region_name}`` was given and does not match either of ``region``
   or ``region_id``, discard the endpoint.

If there are no remaining endpoints, return an error that there are no
endpoints matching ``{region_name}``, preferrably including the list of
regions that were found.

The remaining ``{candidate-endpoints}`` match the request.

If there is more than one of them, select the ones that match the highest
priority ``{interface}``.

If there is more than one of them, return the first, but emit a warning to the
user that more than one endpoint was left. If ``{be-strict}`` has been
requested, return an error instead with information about each of the endpoints
left in the list.

.. note:: It would be more correct to throw an error if there is more than one
          endpoint left, but the keystoneauth library returns the first and
          changing that would break a large number of existing users. If one
          is writing a completely new library from scratch, or a new major
          version where behavior change is acceptable, defaulting to throwing
          an error here if there is more than one version left is preferred.

#. If v2, the ``{catalog-endpoint}`` is the value of ``{interface}URL``.

#. If v3, the ``{catalog-endpoint}`` is the value of ``url``.
