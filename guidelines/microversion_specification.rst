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
  ** A number of endpoints get replaced by others
  ** Drastic changes in API consumer workflow
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

TBD

Version Discovery
-----------------

TBD
