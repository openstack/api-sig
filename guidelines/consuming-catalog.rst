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

.. _catalog-user-request:

User Request
============

.. note:: It is worth noting that 'user' is a maleable concept. For instance,
          the shade library performs service discovery on behalf of its users
          so does not expect its users to provide a 'service-type'. In that
          case, shade is the 'user' of the keystoneauth library which is the
          discovery implementation. It is definitely not required that all
          consumers of OpenStack clouds know all of these things.

The ultimate goal of this process is for a user to find the information about
an endpoint for a service given some inputs. The user will start the process
knowing some number of these parameters. Each additional input expected from
the user without an answer of "where do they learn this information" will
increase the difficulty of a user consuming services, so client libraries and
utilities are strongly encouraged to do whatever they can to be extra helpful
in helping the user ask the right question.

.. note:: Be liberal with what you accept and strict with what you emit.

The following is a list of such pieces of information that can be provided
as user input. When an implementation exposes the ability for a user to
express these parameters it is **STRONGLY** recommended that these names
be used, as they show up across the OpenStack ecosystem and make discussion
easier.

It is assumed that the user has an ``{auth-url}`` and authentication
information. The authentication process itself is out of the scope of this
document.

Required Inputs
---------------

There is one piece of information that is absolutely required that the
user know.

``service-type``
  The official name of the service, such as ``compute``, ``image`` or
  ``block-storage`` as listed in the :doc:`OpenStack Service Types Authority
  <consuming-catalog/authority>`.
  Required. It is impossible for a user to consume service discovery without
  knowing what service they want to discover.

Optional Filters
----------------

There are several optional pieces of information that the user might know,
or additional constraints the user might wish to express to control how the
endpoints for a service are selected.

``region-name``
  The region of the service the user desires to work with. May be optional,
  depending on whether the cloud has more than one region. Services
  all exist within regions, but some clouds only have one region.
  If ``{be-strict}`` (see below) has been given, ``{region-name}`` is required.

  .. note:: It is highly recommended that ``{region-name}`` always be required
            to protect against single-region clouds adding a region in the
            future. However, the canonical OpenStack implementation
            *keystoneauth* today allows region name to be omitted and there are
            a large number of clouds in existence with a single region named
            ``RegionOne``.  For completely new libraries or major versions
            where breaking behavior is acceptable, requiring region name
            by default would be preferred, but breaking users just to introduce
            the restriction is discouraged.

``interface``
  Which API interface, such as ``public``, ``internal`` or ``admin``, that
  the user wants to use. A user should be able to request a list of interfaces
  they find acceptable in the order of their preference, such as
  ``['internal', 'public']`` (Optional, defaults to ``public``)

``endpoint-version`` OR ``min-endpoint-version``, ``max-endpoint-version``
  The **major** version of the service the user desires to work with. Optional.

  An endpoint version is inherently a range with a minimum and a maximum value.
  Whether it is presented to the user as a single parameter or a pair of
  parameters is an implementation detail.

  Each endpoint version is a string with one (``3``) or two (``3.1``) numbers,
  separated by a dot.

  .. warning:: Care has to be taken to not confuse major versions consisting
               of two numbers with microversions. Microversions usually exist
               within a certain major version, and also have a form of ``X.Y``.
               No services currently use both major versions and microversions
               in the form of ``X.Y``.

  .. TODO(dtantsur): so, what if a service has both major versions in the form
                     of ``X.Y`` and microversions?

  Version strings are not decimals, the are a tuple of 2 numbers combined with
  a dot. Therefore, ``3.10`` is higher than ``3.9``.

  A user can omit the endpoint-version indicating that they want to use
  whatever endpoint is in the ``{service-catalog}``.

  A user can desire to work with the latest available version, in which
  case the ``{endpoint-version}`` should be ``latest``. If s
  ``{min-endpoint-version}`` is ``latest``, ``{max-endpoint-version}`` must be
  omitted or also ``latest``.

  A version can be specified with a minor value of ``latest`` to indicate
  the highest minor version of a given major version. For instance,
  ``3.latest`` would match the highest of ``3.3`` and ``3.4`` but not ``4.0``.

  If the parameter is presented as a single string, a single value should be
  interpreted as if ``{min-endpoint-version}`` is the value given and
  ``{max-endpoint-version}`` is ``MAJOR.latest``. For instance, if ``3.4`` is
  given as a single value, ``{min-endpoint-version}`` is ``3.4`` and
  ``{max-endpoint-version}`` is ``3.latest``.

  It may seem strange from an individual user perspective to want a range or
  ``latest`` - but from a library and framework perspective, things like shade
  or terraform may have internal logic that can handle more than one version of
  a service and want to use the best version available.

  .. note:: Guidance around 'latest' is different from that found in
            :ref:`the microversion specification
            <microversion-client-interaction>`. It is acceptable for a client
            library or framework to be interested in the latest version
            available but such a specification is internal and not sent to
            the server. In the client case with major versions, ``latest`` acts
            as an input to the version discovery process.

``service-name``
  Arbitrary name given to the service by the deployer. Optional.

  .. note:: In all except the most extreme cases this should never be needed
            and its use as a meaningful identifier by Deployers is strongly
            discouraged. However, the Consumer has no way to otherwise mitigate
            the situation if their Deployer has provided them with a catalog
            where a ``service-name`` must be used, so ``service-name`` must be
            accepted as input.
            If ``{be-strict}`` (see below) has been requested, a user supplying
            ``{service-name}`` should be an error.

``service-id``
  Unique identifier for an endpoint in the catalog. Optional.

  .. note:: On clouds with well-formed catalogs ``service-id`` should never be
            needed. If ``{be-strict}`` has been requested, supplying
            ``{service-id}`` should be an error.

``endpoint-override``
  An endpoint for the service that the user has procured from some other
  source. (Optional, defaults to omitted.)

Discovery Behavior Modifiers
----------------------------

The user may also wish to express alterations to the general algorithm.
Implementations may present these flags under any name that makes sense,
or may choose to not present them as behavioral modification options at all.

``be-strict``
  Forgo leniant backwards compatibility concessions and be more strict in
  input and output validation. Defaults to False.

``skip-discovery``
  If the user wants to completely skip the version discovery process even if
  logic would otherwise do it. This is useful if the user has specified an
  ``{endpoint-override}`` or they know they just want to use whatever is in
  the catalog and do not need additional metadata about the endpoint. Defaults
  to False

``fetch-version-information``
  If the user has specified an ``{endpoint-version}`` which can be known to
  match just from looking at the URL, the version discovery process will not
  fetch version information documents. However, the user may need the
  information, such as microversion ranges. Using
  ``{fetch-version-information}`` allows them to request that the version
  document be fetched even when an optimization in the process would otherwise
  allow fetching the document to be skipped. Defaults to False.


Discovery Results
=================

At the end of the discovery process, the user should know the following:

If the process was successful:

* The actual values found for all of the input values above.

  Found values will be referred to in these documents as ``found-{value}`` to
  differentiate. So if a user requested an ``{endpoint-version}`` of
  ``latest``, ``{found-endpoint-version}`` might be ``3.5``.

* ``service-endpoint``
  The endpoint to use as the root of the service.

* ``max-version``
  If the service supports microversions, what is the maximum microversion the
  service supports. Optional, defaults to omitted, which implies that
  microversions are not supported.

* ``min-version``
  If the service supports microversions, what is the minimum microversion the
  service supports. Optional, defaults to omitted, which implies that
  microversions are not supported.

If the process was unsuccessful, an error should be returned explaining which
part failed. For instance, was a matching service not found at all or was
a matching version not found. If a matching version was not found, the error
should contain a list of version that were found.

In the description that follows, each of the above inputs and outputs will
be referred to like ``{endpoint-override}`` so that it is clear whether a user
supplied input to the process or one of the expected outputs is being
discussed. Other values that are fetched at one point in the process and
referred to at a later point are similarly referred to like
``{service-catalog}``. Names will not be reused within the process to
hold different content at different times.

Discovery Algorithm
===================

Services should be registered in the ``{service-catalog}`` using their
``{service-type}`` from the :doc:`OpenStack Service Types Authority
<consuming-catalog/authority>`. However, for historical reasons there are some
services that have old service types found in the wild. To facilitate moving
forward with the correct ``{service-type}`` names, but also support existing
users and installations, the OpenStack Service Types Authority contains a list
of historical aliases for such services.

Clients will need a copy of the data published in the
OpenStack Service Types Authority to be able to complete the full Discovery
Algorithm. A client library could either keep a local copy or fetch the data
from https://service-types.openstack.org/service-types.json and potentially
cache it. It is recommended that client libraries handle consumption of the
historical data for their users but also allow some mechanism for the user to
provide a more up to date verison of the data if necessary.

The basic process is:

#. Authenticate to keystone at the ``{auth-url}``, retreiving a ``token``
   which contains the ``{service-catalog}``.

   .. note:: This step is obviously skipped for clouds without authentication.

#. If the user has provided ``{endpoint-override}``, it is used as
   ``{catalog-endpoint}``.

#. If the user has not provided ``{endpoint-override}``, retrieve matching
   ``{catalog-endpoint}`` from the ``{service-catalog}`` using the procedure
   explained in :doc:`consuming-catalog/endpoint`.

#. If ``{skip-discovery}`` is true, STOP and use ``{catalog-endpoint}`` as
   ``{service-endpoint}``. Otherwise, discover the available API versions
   and find the suitable ``{service-endpoint}`` using the version discovery
   procedure from :doc:`consuming-catalog/version-discovery`.

#. If the requested ``{service-type}`` is an alias of an official type in the
   OpenStack Service Types Authority and any endpoints match the official
   type, :ref:`find-endpoint-matching-best-service-type`.


Table of Contents
=================

.. toctree::

   consuming-catalog/endpoint
   consuming-catalog/version-discovery
   consuming-catalog/authority
