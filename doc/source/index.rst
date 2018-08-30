.. api-wg documentation master file

====================================
OpenStack API Special Interest Group
====================================

Mission Statement
-----------------

To improve the developer experience of API users by converging the OpenStack
API to a consistent and pragmatic RESTful design. The working group creates
guidelines that all OpenStack projects should follow for new development, and
promotes convergence of new APIs and future versions of existing APIs.

Preamble
--------

This document contains the guidelines and rules for OpenStack project
APIs including guidelines and proposed rules concerning API consistency, naming
conventions, and best practice recommendations.

If you would like to connect with the API Special Interest Group, visit the
wiki at: https://wiki.openstack.org/wiki/API_Special_Interest_Group

If you are interested in contributing to this document, the git repository is
available at: http://git.openstack.org/cgit/openstack/api-sig/

OpenStack code and review submission processes are described at:
http://docs.openstack.org/infra/manual/developers.html


.. warning::
    These documents from the API Special Interest Group are primarily focused
    on providing advice and guidelines for JSON-based APIs. While other
    representations have their place in the OpenStack ecosystem, they present
    such a diversity of challenges and edge cases, especially with large and/or
    binary request and response bodies, that it is impossible to provide
    guidance that is complete.

.. note::
    Where this guidance is incomplete or ambiguous, refer to the HTTP
    RFCs—:rfc:`7230`, :rfc:`7231`, :rfc:`7232`, :rfc:`7233`, :rfc:`7234`, and
    :rfc:`7235`—as the ultimate authority. For advice on effectively using
    HTTP in APIs see `Building Protocols with
    HTTP <https://tools.ietf.org/id/draft-ietf-httpbis-bcp56bis-06.html>`_.

Guidelines
----------

The following topics are related to the working group and its processes:

.. toctree::
   :glob:
   :maxdepth: 1

   process
   template
   liaisons
   guidedreview

These topics are the API guidance approved by the OpenStack community
and published by the working group:

.. toctree::
   :glob:
   :maxdepth: 1

   guidelines/*
