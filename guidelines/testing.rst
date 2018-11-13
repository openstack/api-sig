Testing
=======

This topic document serves to provide guidance on how to consistently
and effectively test a project's public HTTP API.

Current State of Testing
------------------------

**TODO** Enumerate the variety of HTTP API testing styles and systems
used throughout OpenStack APIs.

Goals
-----

There are many aspects to testing and at least as many stakeholders in
their creation and use. Tests can operate at least three levels:

1. To validate or assist in the creation of new functionality or changes
   to existing code.
2. To prevent regressions.
3. To allow inspection and analysis of the system being tested.

API tests should strive to enable each of these without limiting the
others.

Proposals
---------

1. Each project should have a suite of declarative tests which
   exercise the full breadth of the API, closely mirroring the HTTP
   requests and responses. Being declarative allows easy inspection
   for those who wish to create or understand clients of the service.
   It is also instructive in revealing a certain lack of grace in API
   construction which can be obscured by code-based tests.

2. Black-box testing of APIs is desirable. They do not strictly require
   a web service to be run. WSGI applications can be called directly
   with constructed environments, or using intercepts.

3. **your input here**
