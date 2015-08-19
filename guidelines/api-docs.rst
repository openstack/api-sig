API Documentation
=================

By providing guidelines for API documentation for all OpenStack services,
projects use common tooling, consistent outlines, and study exemplary examples
to meet expectations for API documentation.

Content
-------

First you should generate or write the reference information including:

- Method (GET/PUT/POST/PATCH/HEAD/DELETE)
- Resource (Identified by the URL)
- Request parameters, type and description including whether it
  is optional
- Request headers including media-type, content-type, accept, and others
- Response headers (for some APIs)
- Responses including types and description
- Example request body and headers
- Example response body and headers
- Status codes: successful request and error responses
- Resource model: describes data types that can be consumed and produced by
  operations. This can be through the `Swagger Definitions object <https://github.com/swagger-api/swagger-spec/blob/master/versions/2.0.md#definitionsObject>`_

For this reference information, use the `Swagger 2.0 specification <https://github.com/swagger-api/swagger-spec/blob/master/versions/2.0.md>`_. See
authoring tools below for more information on writing or generating the Swagger
document.

Also important is the conceptual or narrative information that explains the
REST API and what it provides as a service.

Documentation should also offer information about the concepts for each
resource, such as server status or volume status.

Documentation should provide a discussion about the consistency model the
service provides and synchronous or asynchronous behavior for certain methods.

As guidance, here is a list of topics to ensure you include in your API docs
beyond the Swagger reference information.

 * Authentication
 * Faults (synchronous and asynchronous)
 * Limits (rate limits, absolute limits, calls to find out limits)
 * Constraints (min and max for certain values even if chosen by provider)
 * Content compression
 * Encoding
 * Links and references
 * Pagination
 * Filtering
 * Sorting
 * Formats (request, response)
 * Endpoints, versions and discoverability
 * Capabilities and discoverability
 * Term definitions
   (by adding to the OpenStack glossary sourced in openstack-manuals)
 * Status or state values
 * Hierarchy information
 * Quotas
 * Extensions

These topics should be written in RST and built with either Sphinx or alongside
the generated Swagger using the Pecan app described below. The outline itself
is not prescribed since REST APIs vary widely.

Authoring tools
---------------

What is Swagger? `Swagger <http://swagger.io/community/>`_ is a
community-maintained standard for REST API design
and documentation with open-source tooling. Swagger can be written in a YAML
format and then downloaded as a converted JSON file. It allows for inclusion of
content similar to our current entities. To output the information you must run
a server that renders the content. The current community-maintained
`specification for Swagger is version 2.0
<https://github.com/swagger-api/swagger-spec/blob/master/versions/2.0.md>`_.

The centralized OpenStack documentation team works on common tooling for
migrating from WADL to Swagger. See https://github.com/russell/fairy-slipper.

In addition, there's a Pecan decorator proof-of-concept for creating Swagger
when using a Pecan app. See https://github.com/elmiko/pecan-swagger.

Publishing tools
----------------

Within the repo at `fairy-slipper <https://github.com/russell/fairy-slipper>`_
running the Pecan web app can serve RST and Swagger documentation but that
tooling is not yet completed.

The existing OpenStack infrastructure provides publishing to docs.openstack.org
and developer.openstack.org and specs.openstack.org from RST/Sphinx. Running
`tox -e docs` builds Sphinx documentation locally.
