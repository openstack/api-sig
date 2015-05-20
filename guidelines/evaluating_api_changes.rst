..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

======================
Evaluating API Changes
======================

This guideline provides help to developers, core reviewers, and QA
engineers on evaluating whether a given API-impacting change is acceptable
with respect to the OpenStack governance policy on API stability[1].

.. note::

    As of May 2015 this guideline captures historical stances on
    evaluating API changes as they were defined on the OpenStack wiki.

Guidance
========

The following types of changes are generally considered acceptable:

* The change is the only way to fix a security bug.
* Fixing a bug so that a request which resulted in an error response before
  is now successful.
* Adding a new response header.
* Changing an error response code to be more accurate.

The following types of changes are acceptable when conditionally added as a
new API extension:

* Adding a property to a resource representation.
* Adding an optional property to a resource representation which may be
  supplied by clients, assuming the API previously would ignore this property.

The following types of changes are generally **not** considered acceptable:

* A change such that a request which was successful before now results in an
  error response (unless the success reported previously was hiding an
  existing error condition).
* Changing or removing a property in a resource representation.
* Changing the semantics of a property in a resource representation which
  may be supplied by clients.
* Changing or removing a response header.
* Changing which response code is returned on success.

You may feel a particular case is special and warrants an incompatible API
change. Please consider these responses to commonly used justifications:

*"The change is needed to improve API consistency."*

Your desire to improve API consistency is appreciated, but all APIs have
warts. Inconsistencies that need breaking changes can be fixed in a new API
version. Please find a way to channel your efforts into preparations to fix
these consistencies in the next API version.

*"It is unlikely that any existing users of the API would be affected."*

It is difficult to predict how people are using the APIs. Developers do the
strangest things. As our APIs become more adopted over time, it will only
become more futile to attempt to make such predictions. One thing you can
do is to help improve our documentation about how our APIs should be used.
If we can document in future versions that we do not make guarantees about
certain behaviours, that may give us some small additional leeway when it
comes to making changes.

*"The existing API is not well documented."*

If an API's behavior isn't adequately documented, then developers using
the API have no choice but to go by what they observe the behavior to be.

*"The change does not impact users of OpenStack's client libraries or
command line interfaces."*

We encourage developers to develop against OpenStack REST API. There will
be many tools and applications which favor the REST API over our libraries
or command line interfaces.

Examples
========

The following examples represent a selection of appropriately implemented
API changes based on the guidance provided in this document.

**Failing silently**

At one point the change password nova API would return success even if the
system was unable to do it. This made sense to fix because any client
checking the response code of this request surely wants to know if the
request failed. Any existing client which this change affects was broken
anyway because it was failing to actually change the admin password.

* Launchpad bug - `[novaclient] root-password fails and does not return
  error <https://bugs.launchpad.net/nova/+bug/1038227>`_

**Out of spec features belong in extensions**

The ``config_drive`` attribute on servers is not part of the 1.1 Compute API
spec, so it was moved into an extension which could be disabled.

* Launchpad bug - `OSAPI v1.1 needs to document config-drive as an
  extension <https://bugs.launchpad.net/nova/+bug/833331>`_

**Adding new header OK; changing response code not so much**

Rather than returning "200 OK" for successful volume creation, we should
return "201 Created" and include a ``Location`` header. It was decided that
it is safe to add the ``Location`` header, but not change the response code.

* Launchpad bug -  `Volume creation 201 API response does not include a
  Location header <https://bugs.launchpad.net/nova/+bug/1026600>`_

**Inappropriate extension**

Sometimes you come across an extension that makes no sense and is highly
unlikely to be used by anyone.

* Launchpad blueprint -  `Deprecate CreateServerExt extension
  <https://blueprints.launchpad.net/nova/+spec/deprecate-createserverext>`_

**Bugfixes OK**

Fixing incorrect counting of hosts in instance usage audit log.

* Launchpad bug - `Instance usage audit log extension miscounts hosts
  <https://bugs.launchpad.net/nova/+bug/1030106>`_

**Extension aliases**

* Gerrit review - `Make extension aliases consistent
  <https://review.openstack.org/#/c/10812/>`_

**500 error**

* Launchpad bug - `Server create with malformed body yields a 500 error
  <https://bugs.launchpad.net/nova/+bug/1035120>`_
* Launchpad bug - `malformed server update causes: KeyError: 'server'
  <https://bugs.launchpad.net/nova/+bug/1038227>`_

**Inconsistent handling of volume attach device**

* Gerrit review - `Allow nova to guess device if not passed to attach
  <https://review.openstack.org/#/c/10908/>`_

**Missing Property From XML Representation**

* Launchpad bug - `hypervisor_hostname in extended server status doesn't
  appear in xml <https://bugs.launchpad.net/nova/+bug/1039276>`_

References
==========

[1]: https://wiki.openstack.org/wiki/Governance/Approved/APIStability

Mailing list discussion, "Standardizing status codes in the native API
(July 2012)".
http://lists.openstack.org/pipermail/openstack-dev/2012-July/thread.html#132
