.. api-wg documentation master file

===========================
OpenStack API Working Group
===========================

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

If you would like to connect with the API Working Group, visit the wiki at:
https://wiki.openstack.org/wiki/API_Working_Group

If you are interested in contributing to this document, the git repository is
available at: http://git.openstack.org/cgit/openstack/api-wg/

OpenStack code and review submission processes are described at:
http://docs.openstack.org/infra/manual/developers.html


.. warning::
    These documents from the API Working Group are primarily focused on
    providing advice and guidelines for JSON-based APIs. While other
    representations have their place in the OpenStack ecosystem, they present
    such a diversity of challenges and edge cases, especially with large
    and/or binary request and response bodies, that it is impossible to
    provide guidance that is complete. Where there is doubt refer to the
    HTTP RFCs, 7230 through 7235, as the ultimate authority.

Guidelines
----------

The following topics have separate doc pages that contain guidance on a
specific issue:

.. toctree::
   :glob:
   :maxdepth: 1

   process
   template
   liaisons
   guidelines/*
