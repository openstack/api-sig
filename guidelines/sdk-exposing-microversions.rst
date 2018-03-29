Exposing microversions in SDKs
==============================

While we are striving to design OpenStack API as easy to use as possible, SDKs
for various programming languages will always be an important part of
experience for developers, consuming it. This documentation contains
recommendations on how to deal with :doc:`microversions
<microversion_specification>` in SDKs (software development kits)
targeting OpenStack.

This document recognizes two types of deliverables that we usually call SDKs.
They will differ in the recommended approaches to exposing microversions
to their consumers.

* `High-level SDK`_ or just `SDK` is one that hides details of the underlying
  API from consumers, building its own abstraction layers. Its approach
  to backward and forward compatibility, as well as feature discovery, is
  independent of the one used by the underlying API. Shade_ is an example of
  such SDK for OpenStack.

* `Language binding`_ closely follows the structure and design of the
  underlying API. It usually tries to build as little additional
  abstraction layers on top of the underlying API as possible. Examples
  include all OpenStack ``python-<service-name>client`` libraries.

.. note::
    If in doubt, you should write a high-level SDK. The benefit of using an
    SDK is in consuming API in a way, natural to the programming language and
    any used frameworks. Things like microversions are likely to look foreign
    and confusing for developers who do not specialize on API design.

Concepts used in this document:

consumer
    programming code that interfaces with an SDK, as well as its author.
microversion
    API version as defined in :doc:microversion_specification. For simplicity,
    this guideline uses `version` as a synonym of `microversion`.

    .. note::
        When using the word ``microversion`` in your SDK, be careful to avoid
        associations with semantic versioning. A microversion is not the same
        as a patch version, and can be even major in a sense of semantic
        versioning.
major version
    is not really an API version in a sense of :doc:microversion_specification,
    but rather a separate generation of the API, co-existing with other
    generations in the same HTTP endpoints tree.

    Major versions are distinguished in the URLs by ``/v<NUMBER>`` parts and
    are the first components of a microversion. For example, in microversion
    ``1.42``, ``1`` is a major version.

    .. note::
        We don't seem to have an established name for the second component.

    As major versions may change the structure of API substantially, including
    changing the very mechanism of the microversioning, an SDK should generally
    try to stay within the requested major version, if any.
negotiation
    process of agreeing on the most suitable common version between the client
    and the server. Negotiation should happen once, and its results should be
    cached for the whole session.

.. note::
    We will use the Python programming language in all examples, but
    the recommendations will apply to any programming languages, including
    statically compiled ones. For examples here we will use
    a fictional Cats-as-a-Service API and its ``python-catsclient`` SDK.

.. _Shade: https://docs.openstack.org/shade/latest/

High-level SDK
--------------

Generally, SDKs should not expose underlying API microversions to users.
The structure of input and output data should not depend on the microversion
used. Means, specific to the programming language and/or data formats in use,
should be employed to indicate absence or presence of certain features
and behaviors.

    For example, a field, missing in the current microversion, can be
    expressed by ``None`` value in Python, ``null`` value in Java or its type
    can be ``Option<ActualDataType>`` in Rust:

    .. code-block:: python

        import catsclient

        sdk = catsclient.SDK()

        cat = sdk.get_cat('fluffy')
        if cat.color is None:
            print("Cat colors are not supported by this cat server")
        else:
            print("The cat is", cat.color)

    In this example, the SDK negotiates the API microversion that can return
    as much information as possible during the ``get_cat`` call. If the
    resulting version does not contain the ``color`` field, it is set to
    ``None``.

An SDK should negotiate the highest microversion that will allow it to serve
consumer's needs better. However, it should never negotiate a microversion
outside of the range it was written and tested with to avoid confusing
breakages on future changes to the API. It goes without saying that an SDK
should not crush or exhibit undefined behavior on any microversion returned
by a server. Any incompatibilities should be expressed as soon as possible
in a form that is natural for the given programming language.

    For example, a Python SDK should raise an exception when a method is
    called that is not possible to express in any microversion supported by
    both the SDK and the server:

    .. code-block:: python

        import catsclient

        sdk = catsclient.SDK()

        cat = sdk.get_cat('fluffy')
        try:
            cat.bark()
        except catsclient.UnsupportedFeature:
            cat.meow()

    It is also useful to allow detecting supported features before
    using them:

    .. code-block:: python

        import catsclient

        sdk = catsclient.SDK()

        cat = sdk.get_cat('fluffy')
        if cat.can_bark():
            cat.bark()
        else:
            cat.meow()

    In this example, ``can_bark`` uses the negotiated microversion to check if
    it is possible for the ``bark`` call to work.

.. note::
    If possible, an SDK should inform the consumer of the required API
    microversion and why it is not possible to use it. This is probably the
    only place where microversions can and should leak to a consumer.

If possible, major versions should be treated the same way, and should not be
exposed to users. If not possible, an SDK should pick the most recent
major version from the available.

Language binding
----------------

A low-level SDKs, which is essentially just a language binding for the API,
stays close to the underlying API. Thus, it must expose microversions
to consumers, and must do it in a way, closest to how API does it. We
recommend that all calls accept an explicit API microversion that is sent
directly to the underlying API. If none is provided, no version should be sent:

.. code-block:: python

    import catsclient

    client = catsclient.v1.get_client()

    cat = client.get_cat('fluffy')  # executed with no explicit version
    try:
        cat.bark(api_version='1.42')  # executed with 1.42
    except catsclient.IncompatibleApiVersion:
        # no support for 1.42, falling back to older behavior
        cat.meow()  # executed with no explicit version

.. note::
    In some programming languages, particularly those without default arguments
    for functions, it may be inconvenient to add a version argument to all
    calls. Other means may be used to achieve the same result, for example,
    temporary context objects:

    .. code-block:: python

        import catsclient

        client = catsclient.v1.get_client()

        cat = client.get_cat('fluffy')  # executed with no explicit version
        with cat.use_api_version('1.42') as new_cat:
            new_cat.bark()  # executed with 1.42

Major versions
~~~~~~~~~~~~~~

A low-level SDK should make it explicit which major version it is working
with. It can be done by namespacing the API or by accepting an explicit
major version as an argument. The preferred approach depends on how
different the major versions of an API are.

Using Python as an example, either

.. code-block:: python

    import catsclient
    client = catsclient.v1.get_client()

or

.. code-block:: python

    import catsclient
    client = catsclient.get_client(1)

Supported versions
~~~~~~~~~~~~~~~~~~

It's highly recommended to provide a way to query the server for the
supported version range:

.. code-block:: python

    import catsclient

    client = catsclient.v1.get_client()
    min_version, max_version = client.supported_api_versions()

    cat = client.get_cat('fluffy')  # executed with no explicit version
    if max_version >= (1, 42):
        cat.bark(api_version='1.42')  # executed with 1.42
    else:
        # no support for 1.42, falling back to older behavior
        cat.meow()  # executed with no explicit version

Minimum version
~~~~~~~~~~~~~~~

Applications often have a base minimum API version they are capable of working
with. It is recommended to provide a way to accept such version and use it
as a default when no explicit version is provided:

.. code-block:: python

    import catsclient

    try:
        client = catsclient.v1.get_client(api_version='1.2')
    except catsclient.IncompatibleApiVersion:
        sys.exit("Cat API version 1.2 is not supported")

    cat = client.get_cat('fluffy')  # executed with version 1.2
    try:
        cat.bark(api_version='1.42')  # executed with 1.42
    except catsclient.IncompatibleApiVersion:
        # no support for 1.42, falling back to older behavior
        cat.meow()  # executed with version 1.2

As in this example, an SDK using this approach must provide a clear way to
indicate that the requested version is not supported and do it as early as
possible.

List of versions
~~~~~~~~~~~~~~~~

As a simplification extension, a language binding may accept a list of versions
as a base version. The highest version supported by the server must be picked
and used as a default.

.. code-block:: python

    import catsclient

    try:
        client = catsclient.v1.get_client(api_version=['1.0', '1.42'])
    except catsclient.IncompatibleApiVersion:
        sys.exit("Neither Cat API 1.0 nor 1.42 is supported")

    cat = client.get_cat('fluffy')  # executed with either 1.0 or 1.42
                                    # whichever is available
    if client.current_api_version == (1, 42):
        # Here we know that the negotiated version is 1.42
        cat.bark()  # executes with 1.42
    else:
        # Here we know that the negotiated version is 1.0
        cat.meow()  # executes with 1.0

    # The default version can still be overwritten
    try:
        cat.drink(catsclient.MILK, api_version='1.66')  # executed with 1.66
    except catsclient.IncompatibleApiVersion:
        # no support for 1.66, falling back to older behavior
        cat.drink()  # executed with either 1.0 or 1.42 whichever is available
