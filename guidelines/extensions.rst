.. _extensions:

API Extensions
==============

This topic document serves to provide guidance on the topic of API extensions.

See also the topic documents on :ref:`discoverability` and
:ref:`interoperability`.

Guidance
--------

API extensions are sometimes used to add custom functionality to single
deployments of OpenStack. They are not recommended, because when they are
used, they break interoperability between that cloud and other OpenStack
deployments.

If a deployment requires custom behaviors over an HTTP API it should be
implemented in a service separate from the existing OpenStack services.

Those projects that support different functionality based on the presence
of drivers should strive to contain those differences to the values (not keys)
in representation objects. Having different URLs in a service, based on
different drivers, breaks interoperability. Where such functionality is
absolutely required then it is critical that the functionality be discoverable
via a capabilities API.

.. note:: At this time the standards and best practices for capabilities
          discovery are undefined.
