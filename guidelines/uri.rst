..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode


==============
Effective URIs
==============

Effective URIs (also sometimes referred to by the somewhat more specific term
URL [#url]_) are central to the design of a usable HTTP API. Uniform
Resource Identifiers are defined by :rfc:`3986` and have their use
in HTTP clarified in :rfc:`7230#section-2.7`. A URI is the identifier
of a resource in an API and is also used to locate and address that
resource on network.

A URI is divided up into several sections: `scheme`, `authority`, `path`,
`query`, and `fragment` (please refer to :rfc:`3986` for more detail).
As a developer of API services, `path` and `query` are most relevant;
`fragment` is not usually sent to the service and there is little
opportunity nor reason to exert control over `scheme` and
`authority`.

What follows will concern itself solely with the `path` and `query`.

Things Worth Knowing
--------------------

* The value of `path` and `query` are case sensitive. That is if you
  have two URIs that look similar,
  ``http://example.com/foo/BAR?dEtail=1``
  and ``http://example.com/foo/bar?detail=1``, they are not
  equivalent. A server application can choose to normalize the URI
  but this not recommended as it does not correspond with common
  use nor :rfc:`7230#section-2.7.3`.

* While a `path` often looks like a hierarchical path
  (``/collection/item/sub-resource/detail``), akin to the
  full filename of a file on disk, this is a matter of convenience
  and an artifact of making the URI consumable by humans. The truth
  of the matter is that the entirety of the URI identifies the
  resource, not just the last segment of the path.

* The entire point of URI design [#exitclause]_ is to make the URIs
  consumable by humans in a meaningful fashion both for users of the
  API and future maintainers of the API.

General Advice on URI Design
----------------------------

.. note:: This is far from an exhaustive list. This is merely a
   starting point from which we can accumulate reasonable advice on
   how to form good URIs.

* Since a single URI identifies a single resource it is also useful
  for two more things to be kept true when building services:

  * Any resource should only have one URI. Where possible do not provide
    multiple ways to reference the same thing. Use HTTP redirects to
    resolve indirect requests to the correct canonical URI and
    content negotiation to request different representations.

  * Any given resource, since it should only have one URI, should
    respond to all relevant HTTP methods at just that URI and not have
    secondary URIs for some methods. For example:

    Use::

        GET /resources/1322b203bdc64c13b6e72b04d43e8690
        DELETE /resources/1322b203bdc64c13b6e72b04d43e8690

    Never::

        GET /resources/1322b203bdc64c13b6e72b04d43e8690
        DELETE /resources/1322b203bdc64c13b6e72b04d43e8690/delete

* It is often the case that an API will have URIs that
  :doc:`represent collections <representation_structure>` for resources
  and individual members of that collection in a hierarchy. For example
  [#non-normative]_::

    GET /birds

    {"birds": [
        {
            "name": "alpha",
            "type": "crow"
        },
        {
            "name": "beta",
            "type": "jackdaw"
        }
    }

    GET /birds/alpha

    {
        "name": "alpha",
        "type": "crow"
    }

  This is a reasonable thing to do as it goes a long way to making
  the elements of an API comprehensible.

* If the hierarchy described above is used it is important that
  all URIs that take the second form (``/birds/alpha``) have the
  same semantics and are always identifying a resource which is a
  member of this collection (in this case "is a bird").

  There are multiple examples throughout OpenStack of this concept
  being violated. For example in the `os-cells` API in nova it is
  possible to ``GET /os-cells`` to get a list of cells, ``GET
  /os-cells/some-name`` to get information about a single cell named
  ``some-name`` and ``GET /os-cells/details`` to get the same
  information as ``GET /os-cells`` but with additional detail.

  For this particular example one way (of several options) to achieve
  the same result while preserving URI semantics would have been to use a
  `query` to augment the existing collection URI to indicate the
  desire for more detail [#non-normative]_::

    GET /os-cells?details=true

  .. todo:: There is an as yet unresolved debate on the best way to indicate
     boolean query parameters. Any of ``details=true``, ``details=1`` or
     ``details`` could make sense here. The above should not be taken to
     indicate support for any `query` format. Rather it is merely to
     demonstrate cleaner semantics in the `path` portion of the URI.

.. rubric:: Footnotes

.. [#url] https://en.wikipedia.org/wiki/Uniform_Resource_Locator
.. [#exitclause] There is another school of thought which insists
   that URIs should be entirely opaque identifiers which computers
   use to exchange information. There's a lot of value in this
   line of thinking as it allows the identifiers to act as
   references to fungible referents, but it discounts the value and cost of
   creating a diverse collection of clients for services. If we
   wish to encourage that diverse collection then having URIs which
   are consumable by humans is helpful.
.. [#non-normative] These are example requests and responses only and
   should not be taken as explicitly describing correct form.
