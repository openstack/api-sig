..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=============================
Ensuring API Interoperability
=============================

The OpenStack mission includes the following goal for OpenStack clouds:
"interoperable between deployments". In the context of HTTP APIs this means
that client code that is written for cloud `A` should also work on cloud
`B` and any other cloud. Because cloud `A` and cloud `B` may be running
different releases of the OpenStack services at any given point in time,
and they may upgrade their services at different points in time, this has
important implications for how API developers add features, fix bugs, and
remove functionality from the service APIs.

If a service wants to ensure (and they should) that client code is always
interoperable with multiple different OpenStack clouds then:

* The changes must not violate compatibility nor stability, both of which
  are defined in more detail below.

* Changes in resources and request and response bodies and headers are not
  allowed without signalling a version boundary, except in a very small
  number of cases (see below).

  .. note:: APIs which have different behaviors and representations based on
            the availability of different drivers present significant
            challenges for interoperability. Where possible such differences
            should be avoided. Where that's not possible, interoperability
            should be considered when cloud `A` and cloud `B` have the same
            sets of drivers available.

* Version discovery and selection should default to a baseline; making use of
  new features and changes in an API should be opt-in.

* When functionality is fully removed, this must result in the baseline
  being raised. Ideally this should result in the equivalent of a major
  version update because stability (backwards compatibility) has been
  violated. When a service uses microversions, "major version update" often
  means raising the minimum available version.

* If functionality is going to be removed its removal should follow
  standard OpenStack deprecation procedures.

* A service that wants to deprecate some functionality but maintain
  stability is welcome to do so by documenting the functionality as
  deprecated but keeping the functionality present in the API.

The gist here is that any service with a published API that also needs to
make changes to that API (to fix or evolve it) needs to have a mechanism
for versioning. This document does not address versioning, however the
only mechanism in active use in OpenStack that has been demonstrated to
work for the goals described here are :doc:`microversions
<microversion_specification>`.

The rest of this document will describe the rules that a service MUST
follow if it wishes to ensure API interoperability. It makes two
assumptions that are important for understanding the compromises this document
makes:

* Change in APIs is an inevitable consequence of evolving projects with a
  diversity of contributors. In the unlikely event that such change is not
  a consideration then these guidelines need not apply.
* The overarching goal of the API Working Group is to encourage consistency
  in the APIs of all the services. The proposed solutions for enabling
  compatibility and stability are guidance towards achieving consistency.
  The assertions about when a change will violate interoperability are true
  independent of any given solution.

Any service which does not support versioning and wishes to achieve
interoperability SHOULD do two things:

* Add support for versioning.
* Strive to follow these guidelines in a best-faith manner and where not
  possible consider changes with regard to reasonably expected behavior
  in client code.

.. note:: A project which does not have a robust system for managing version
          boundaries but must make changes to their API is by definition not
          adhering to these guidelines for interoperability. The project itself
          must make the decisions on how to evolve their API. If this leads to
          conflicts with other projects within the OpenStack ecosystem, the
          role of the API-WG is solely to help clarify the guidelines and
          provide advice on how to minimize the impact of changes. The
          Technical Committee is the body which provides adjudication and
          mediation when consensus cannot be reached.

Whether a service follows the guidelines or not, any service should always
strive to minimize API changes and version increases as that exacerbates the
need for users to "keep up" with the changes.

A service which is new and under development will obviously be undergoing a
great deal of change in its early days. During this time versioning is
not an indicator or tool for stability. However, once there has been a
release or a dependency created with another service, stability and
compatibility become critical if interoperability is desired.

Definitions
===========

For the sake of these guidelines the terms `compatibility` and `stability`
are given fairly narrow definitions:

**compatibility**
  An API is compatible when client code written for that service on cloud
  `A` will work without changes with the same service on cloud `B`.

**stability**
  An API is stable when client code written at time `X` will continue to
  work without changes at future time `Y`.

These definitions assume that client code is written to follow the
standards of HTTP.

When there is doubt in how these definitions should be applied to a situation
consideration should be given first to the perspective and needs of the end
users of the API (that is, those individuals who wish to use the same code
against multiple clouds), second to the deployers and admins of the clouds,
and third to the developers of the service.

Evaluating API Changes
======================

There are two types of change which **do not** require a version change:

* The change is required to fix a security bug that is so severe that it
  requires backporting to all supported releases of the service.

  This case should be rare. For many less severe security situations the right
  answer is to treat the problem as a bug, make the fix, make a new version and
  release, and suggest people upgrade. The `OpenStack Vulnerability Management
  Team <https://security.openstack.org/#vulnerability-management>`_ has the
  expertise to determine the true severity of a security bug.

* A bug in the API service which results in a client getting a response
  with a status code in the ``500-599`` range being fixed to return an
  informative error response in the ``400-499`` range (when the
  request was erroneous but fixable) or responding with success (when
  the request was properly formed, but the server had broken
  handling).

The following changes **do** require a version change:

* Adding a new URL.

  This may seem backwards-compatible, as old clients would never use
  the new URL, but it breaks interoperability between clouds
  presenting the same version of the API but using different code.

* Changing the response status code from one form of client error to another
  (e.g., ``403`` to ``400``) or one form of success to another (e.g., ``201``
  to ``204``).

  There continues to be debate on this topic with regard to changing success
  codes. A robust client could effectively ride through changes in success if
  it treated anything from ``200`` to ``299`` as success. This requires a
  different standard of client than these guidelines assume. Because there is
  already a great deal of client code out in the OpenStack ecosystem, enforcing
  a client-side standard such as the `tolerant reader`_ concept, is not
  possible.

* Adding or removing a request or response header.

* Changing the value of a response header which would change how the response
  should be processed by the client. For example changing the value of the
  ``Content-Type`` header to add a new media-type.

* Adding or removing a property in a resource representation in either a
  request or a response.

* Changing the semantics or type of an existing property in a resource
  representation (request or response).

* Changing the set of values allowed in a resource property, while
  maintaining its type.

  For example if a property once accepted "foo", "bar", or "baz" and "zoom"
  was added as a legitimate value, that would require a version. If "foo" was
  removed that too would require a version. Both addition and removal are
  relevant here because we want two different clouds at the same API version
  (but with potentially different code releases) to behave the same. To get
  that, even apparently backwards compatible changes require a version change.

The following changes are possible if a version change is made but due
consideration should be given to the impact this will have on existing users.
At some point the user will want access to new functionality that is in higher
versions or the minimum version of the service will be raised beyond the
version where the change happens. The compensating changes in client code will
be significant when any change is made, but especially so for these.

* A change such that a request which was successful before now results in an
  error response (unless the success reported previously was hiding an
  existing error condition).

* Removing a URL.

Examples
========

In many cases it will feel like a change is special and violation of these
guidelines is warranted. Please consider the following scenarios:

*"The change is needed to improve API consistency."*

Your desire to improve API consistency is appreciated and desired, but all
APIs have warts. Inconsistencies that need breaking changes could be fixed in
a new API version but it isn't always necessary. Another option is to add a
new URL with the different behavior. Consider all the options, finding a way
to channel your efforts into improving the overall experience of using the
API.

*"It is unlikely that any existing users of the API would be affected."*

It is difficult to predict how people are using the APIs. Developers do the
strangest things. As our APIs become more adopted over time, it will only
become more futile to attempt to make such predictions. An exception to this
rule is when the functionality being changed is something that was literally
non-functional.

*"The existing API is not well documented."*

If an API's behavior isn't adequately :doc:`documented <api-docs>`, then
developers using the API have no choice but to go by what they observe the
behavior to be. A change that will violate those observations is a change that
requires a version.

*"The change does not impact users of OpenStack's client libraries or
command line interfaces."*

We encourage developers to develop against OpenStack REST API. There will
be many tools and applications which favor the REST API over our libraries
or command line interfaces.

New or Experimental Services and Versioning
===========================================

As stated above, a brand new service should not commit to stability (as
defined here) too early in its development. Only once some form of stability
(in the standard English sense) has been reached is it worth considering.

A project which has an existing stable service that wants to experiment with
new functionality that it may choose to never stabilize should publish that
experimental service at a unique endpoint in the service catalog, separate
from the existing service.

.. _tolerant reader: https://martinfowler.com/bliki/TolerantReader.html

References
==========

* Mailing list discussion, "Standardizing status codes in the native API
  (July 2012)".
  http://lists.openstack.org/pipermail/openstack-dev/2012-July/thread.html#132
* Mailing list discussion, "refreshing and revalidating api compatibility
  guidelines (January 2017)".
  http://lists.openstack.org/pipermail/openstack-dev/2017-January/thread.html#110384
* Blog posting, "Interop API Requirements (February 2017)".
  https://blog.leafe.com/interop-api-requirements/
* The review that created this document.
  https://review.openstack.org/#/c/421846/
