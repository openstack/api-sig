DNS-based Service Discovery
===========================

The normal way to discover OpenStack services is via the :doc:`service catalog
<consuming-catalog>`. However, in some edge cases it may be convenient to use
DNS-based discovery, for example:

#. Initial discovery of the Identity service endpoint via DNS.
#. Discovery of a service on the local network, especially in standalone case.

.. warning::
    This guideline does not endorse any services to implement any DNS-based
    discovery, but rather serves as guidance for services and deployments
    that need it.

This guideline is heavily based on two IETF documents:

* `RFC 6763`_ defines DNS service discovery.
* `RFC 6762`_ defines the Multicast DNS protocol (or mDNS).

Service Type
------------

`RFC 6763`_ section 7 defines a fully qualified domain name for a service in
the following format::

    <instance>.<servicename>._tcp.<domain>.

where:

``domain``
    is a parent domain that the service belong to. It must be ``local`` for
    multicast DNS.
``servicename``
    is a service-specific protocol name, which in case of OpenStack API
    discovery MUST be ``_openstack``.
``instance``
    is an instance of a service, which in case of OpenStack API discovery MUST
    be an OpenStack service type, such as ``compute``, ``identity`` or
    ``baremetal``. Project code names, such as ``nova``, MUST NOT be used.

Service Information
-------------------

The DNS ``SRV`` record will provide a host and port number for the service.
DNS ``TXT`` records SHOULD be used to communicate the remaining parts required
to access a service. `RFC 6763`_ defines the format of these records to be
key-value pairs separated by ``=``. This guideline defines the following keys:

``path``
    SHOULD be used to specify the path part of the endpoint. If missing, ``/``
    MUST be assumed.

    .. note::
        It's tempting to prefix the keys defined here with something like
        ``os_``, but ``path`` is used in the examples in `RFC 6763`_ in exactly
        the same role, so it may be familiar enough to potential consumers
        and tools.
``protocol``
    SHOULD be used to specify whether to use HTTP or HTTPS. If present, it MUST
    be ``http`` or ``https``. If absent, a consumer SHOULD use the port to
    decide which protocol to use:

    * if port is 80, use HTTP,
    * if port is 443, use HTTPS,

    If port is not one of 443 and 80, a consumer SHOULD try HTTPS and MAY fall
    back to HTTP if it fails.
``txtvers``
    SHOULD be used as defined in `RFC 6763`_ to designate the version of the
    format. If present, its value MUST be ``1``.

Examples
--------

Identity discovery for a provider
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As a new user of OpenStack provider ``mystack.example.com``, I would like to
discover the ``auth_url`` to use.

I issue a DNS request to retrieve ``SRV`` and ``TXT`` records::

    $ nslookup -query=any "identity._openstack._tcp.mystack.example.com"
    identity._openstack._tcp.mystack.example.com    service = 0 0 443 os.mystack.example.com
    identity._openstack._tcp.mystack.example.com    text = "txtvers=1" "path=/"

Now I know that I have to connect to ``os.mystack.example.com``, port 443.
From the ``TXT`` records I know that I should use the root path. The protocol
is not specified, so from port 443 I derive using HTTPS.

Result: ``auth_url`` is ``https://os.mystack.example.com/``.

Local discovery of ironic
~~~~~~~~~~~~~~~~~~~~~~~~~

The ironic service ramdisk needs to discover baremetal (ironic) and baremetal
introspection (ironic-inspector) API endpoints after start up. The service
catalog is not available to it.

The ramdisk issues a multicast DNS request to list OpenStack services. An
equivalent Avahi_ (FOSS mDNS and DNS-SD implementation) command would be::

    $ avahi-browse -rt _openstack._tcp
    + eth1 IPv4 baremetal                                     _openstack._tcp      local
    + eth1 IPv4 baremetal-introspection                       _openstack._tcp      local
    = eth1 IPv4 baremetal                                     _openstack._tcp      local
       hostname = [baremetal._openstack._tcp.local]
       address = [192.168.42.17]
       port = [80]
       txt = ["proto=http" "path=/baremetal"]
    = eth1 IPv4 baremetal-introspection                       _openstack._tcp      local
       hostname = [baremetal-introspection._openstack._tcp.local]
       address = [192.168.42.17]
       port = [5050]
       txt = ["proto=http"]

Here we do a multicast search for all services matching service type
``_openstack._tcp`` defined in `Service Type`_. We receive two results for
the expected services, each containing an IP address, a TCP port and ``proto``
and ``path`` variables as part of its ``TXT`` section.

Result:

* The baremetal endpoint is ``http://192.168.42.17/baremetal``.
* The baremetal introspection endpoint is ``http://192.168.42.17:5050``.

.. _RFC 6763: https://www.ietf.org/rfc/rfc6763.txt
.. _RFC 6762: https://www.ietf.org/rfc/rfc6762.txt
.. _Avahi: https://avahi.org/
