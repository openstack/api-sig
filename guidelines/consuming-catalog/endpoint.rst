Endpoint Discovery
==================

Endpoint from Catalog
---------------------

The ``{service-catalog}`` can be found in the ``token`` returned from
keystone authentication.

If v3 auth is used, the catalog will be in the ``catalog`` property of the
top-level ``token`` object. Such as:

.. code-block:: json

  {
    "token": {
      "catalog": {}
    }
  }

If v2 auth is used it will be in the ``serviceCatalog`` property of the
top-level ``access`` object. Such as:

.. code-block:: json

  {
    "access": {
      "serviceCatalog": {}
    }
  }

In both cases, the catalog content itself is a list of objects. Each object has
two main keys that concern discovery:

``type``
  Matches ``{service-type}``

``endpoints``
  List of endpoint objects for that service

Additionally, for backwards compatibility reasons, the following keys may
need to be checked.

``name``
  Matches ``{service-name}``

``id``
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

Examples of Tokens with Catalogs
--------------------------------

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

Endpoint Discovery Algorithm
----------------------------

#. If ``{endpoint-version}`` was given and ``{service-type}`` ends with a
   suffix of ``v[0-9]+$`` and ``{endpoint-version}`` does not match that suffix
   (see `Comparing Major Versions`_), STOP. Return an error that the user
   has requested a versioned ``{service-type}`` alias and an incompatible
   ``{endpoint-version}``.

#. Find the objects in the ``{service-catalog}`` that match the requested
   ``{service-type}`` (see `Match Candidate Entries`_).

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

The list of remaining objects are the ``{candidate-catalog-objects}``. If this
list is empty, return an error that there are no endpoints matching
``{service-type}`` and ``{service-name}``.

#. Use ``{candidate-catalog-objects}`` to produce the list of
   ``{candidate-endpoints}``. For each endpoint object in each of the
   ``{candidate-catalog-objects}``:

   #. If v2, if there is no key of the form ``{interface}URL`` for any of the
      the ``{interface}`` values given, discard the endpoint.

   #. If v3, if ``interface`` does not match any of the ``{interface}`` values
      given, discard the endpoint.

#. If there are no endpoints left, return an error that there are no endpoints
   matching any of the ``{interface}`` values, preferrably including the list
   of interfaces that were found.

#. For each remaining endpoint in ``{candidate-endpoints}``, if
   ``{region_name}`` was given and does not match either of ``region`` or
   ``region_id``, discard the endpoint.

   If there are no remaining endpoints, return an error that there are no
   endpoints matching ``{region_name}``, preferrably including the list of
   regions that were found.

#. From the set of remaining candidate endpoints, find the ones that best
   matches the requested ``{service-type}`` (see `Find Endpoint Matching Best
   Service Type`_).

#. From the set of remaining candidate endpoints, find the ones that best
   matches the best available requested ``{interface}``: in order of
   preference of the ``{interface}`` list, return all endpoints that match
   the first ``{interface}`` that has any matching endpoints.

The remaining ``{candidate-endpoints}`` match the request. If there is more
than one of them, use the first, but emit a warning to the user that more
than one endpoint was left. If ``{be-strict}`` has been requested, return an
error instead with information about each of the endpoints left in the list.

.. note:: It would be more correct to raise an error if there is more than one
          endpoint left, but the keystoneauth library returns the first and
          changing that would break a large number of existing users. If one
          is writing a completely new library from scratch, or a new major
          version where behavior change is acceptable, it is preferable to
          raise an error here if there is more than one endpoint left.

#. If v2, the ``{catalog-endpoint}`` is the value of ``{interface}URL``.

#. If v3, the ``{catalog-endpoint}`` is the value of ``url``.

Match Candidate Entries
~~~~~~~~~~~~~~~~~~~~~~~

For every entry in the catalog:

#. If the entry's type matches the requested ``{service-type}``, it is a
   candidate.

#. If the requested type is an official type from the
   :doc:`OpenStack Service Types Authority <authority>` that has aliases and
   one of the aliases matches the entry's type, it is a candidate.

#. If the requested type is an alias of an official type from the
   :doc:`OpenStack Service Types Authority <authority>` and the entry's type
   matches the official type, it is a candidate.

#. If the requested type is an alias of an official type from the
   :doc:`OpenStack Service Types Authority <authority>` that has aliases and
   the entry's type matches one of the aliases and ``{endpoint-version}`` was
   given and the found alias ends with a suffix of ``v[0-9]+$`` and
   ``{endpoint-version}`` matches the version in the suffix (see `Comparing
   Major Versions`_) it is a candidate.

.. _find-endpoint-matching-best-service-type:

Find Endpoint Matching Best Service Type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Given a list of candidate endpoints that have matched the other criteria:

#. Check the list of candidate endpoints to see if one of them matches the
   requested ``{service-type}``. If any are an exact match, return them.

#. If the requested ``{service-type}``

   * is an official type from the :doc:`OpenStack Service Types Authority
     <authority>` that has aliases
   * ``{endpoint-version}`` was given

   Look for aliases that end with a version suffix of the form ``v[0-9]+$``.
   If there are any aliases with a version suffix that matches the
   ``{endpoint-version}`` (see `Comparing Major Versions`_), look for those
   aliases in the list of candidate endpoints. If any are a match, return them.

#. If the requested ``{service-type}``

   * is an official type in the :doc:`OpenStack Service Types Authority
     <authority>` that has aliases
   * ``{endpoint-version}`` was not given

   check each alias in the order listed to see if it has a matching endpoint
   from the candidate endpoints. Return the endpoints that match the first
   alias that has matching endpoints.

#. If the requested ``{service-type}``

   * is an alias of an official type in the
     :doc:`OpenStack Service Types Authority <authority>`
   * ``{endpoint-version}`` was given

   look for aliases that end with a version suffix of the form ``v[0-9]+$``. If
   there are any aliases with a version suffix that matches the
   ``{endpoint-version}`` (see `Comparing Major Versions`_), look for those
   aliases in the list of candidate endpoints.

   Return the endpoints that match the alias with the highest matching version.

#. If there are no matching endpoints, return an error.

.. note:: The case where

          * an alias was requested
          * no ``{endpoint-version}`` was given
          * there is a different alias in the catalog

          is not safe and so is treated as a lack of matching endpoint on
          purpose. Many of the aliases carry an implied version, so absent
          a requested ``{endpoint-version}`` from the user, returning
          an endpoint different than the one explicitly requested has a high
          chance of not being the endpoint the user expected.

.. _comparing-major-versions:

Comparing Major Versions
~~~~~~~~~~~~~~~~~~~~~~~~

When comparing Major Versions, there is a ``required`` and a ``candidate``:

* The ``required`` is what the user has requested.
* The ``candidate`` is the possible version being tested.

To be suitable a ``candidate`` must be of the same major version as
``required`` and be at least a match in minor level: ``candidate`` ``3.3``
is a match for ``required`` ``3.1`` but ``4.1`` is not.

Leading 'v' strings should be discarded in all cases.

#. Versions with only a single number normalize to ``.0``. That is,
   a version of ``2`` should be treated as if it was ``2.0``.

#. If ``required`` is the string ``latest`` or contains no value, ``candidate``
   matches.

#. If ``required`` is a range, any ``candidate`` that is greater than or equal
   to the first value and less than or equal to the second value is a match.
   Equality is judged by the above rules. Greater than and less than are judged
   as expected: first by comparing the first number, and if those match then by
   comparing the second number.  Thus, a ``{required}`` of ``2,4`` matches
   ``2``, ``2.3``, ``3``, ``4`` and ``4.7``. A ``{required}`` of ``2.1,4.0``
   matches ``2.3``, ``3``, ``4`` and ``4.7`` but not ``2``.

#. If ``required`` is a range without a maximum value, maximum should be
   treated as if it is ``latest``.

Examples of discovery
---------------------

For example, given the following catalog:

.. code-block:: json

  {
    "token": {
      "catalog": [
          {
              "endpoints": [
                  {
                      "interface": "public",
                      "region": "RegionOne",
                      "url": "https://block-storage.example.com/v3"
                  }
              ],
              "id": "4363ae44bdf34a3981fde3b823cb9aa3",
              "type": "volumev3",
              "name": "cinder"
          },
          {
              "endpoints": [
                  {
                      "interface": "public",
                      "region": "RegionOne",
                      "url": "https://block-storage.example.com/v2"
                  }
              ],
              "id": "4363ae44bdf34a3981fde3b823cb9aa2",
              "type": "volumev2",
              "name": "cinder"
          }
      ],
  }

Then the following:

::

  service_type = 'block-storage'
  # block-storage is not found, get list of aliases
  # volumev3 is found, return it

  service_type = 'volumev2'
  # volumev2 not an official type in authority, but is in catalog
  # return volumev2 entry

  service_type = 'volume'
  # volume not in authority or catalog
  # volume is an alias of block-storage
  # block-storage is not found. Return error.

  service_type = 'volume'
  api_version = 2
  # volume not in authority or catalog
  # volume is an alias of block-storage
  # block-storage is not found.
  # volumev2 is an alias of block-storage and ends with v2 which matches
  #   api_version of 2
  # return volumev2

Given the following catalog:

.. code-block:: json

  {
    "token": {
      "catalog": [
          {
              "endpoints": [
                  {
                      "interface": "public",
                      "region": "RegionOne",
                      "url": "https://block-storage.example.com"
                  }
              ],
              "id": "4363ae44bdf34a3981fde3b823cb9aa3",
              "type": "block-storage",
              "name": "cinder"
          }
      ],
  }

Then the following:

::

  service_type = 'block-storage'
  # block-storage is found, return it

  service_type = 'volumev2'
  # volumev2 not in authority, is an alias for block-storage
  # block-storage is in the catalog, return it

  service_type = 'volumev2'
  api_version = '3'
  # volumev2 ends with a version suffix of v2 which does not match 3
  # return an error before even fetching the catalog

Given the following catalog:

.. code-block:: json

  {
    "token": {
      "catalog": [
          {
              "endpoints": [
                  {
                      "interface": "public",
                      "region": "RegionOne",
                      "url": "https://block-storage.example.com"
                  }
              ],
              "id": "4363ae44bdf34a3981fde3b823cb9aa3",
              "type": "block-storage",
              "name": "cinder"
          },
          {
              "endpoints": [
                  {
                      "interface": "public",
                      "region": "RegionOne",
                      "url": "https://block-storage.example.com/v2"
                  },
                  {
                      "interface": "internal",
                      "region": "RegionOne",
                      "url": "https://block-storage.example.int/v2"
                  }
              ],
              "id": "4363ae44bdf34a3981fde3b823cb9aa2",
              "type": "volumev2",
              "name": "cinder"
          }
      ],
  }

Then the following:

::

  service_type = 'block-storage'
  interface = ['internal', 'public']
  # block-storage is found
  # block-storage does not have internal, but has public
  # return block-storage public

  service_type = 'volumev2'
  interface = ['internal', 'public']
  # volumev2 not an official type in authority, but is in catalog
  # volumev2 has an internal interface
  # return volumev2 internal entry

