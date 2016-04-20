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
  operations.

The resource model may be created with either a parameters.yaml file or with
the `OpenAPI Definitions object <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#definitionsObject>`_
Swagger is governed by the OpenAPI initiative.

See authoring tools below for more information on writing or generating the
parameters information.

Also important is the conceptual or narrative information that explains the
REST API and what it provides as a service.

Documentation should also offer information about the concepts for each
resource, such as server status or volume status.

Documentation should provide a discussion about the consistency model the
service provides and synchronous or asynchronous behavior for certain methods.

As guidance, here is a list of topics to ensure you include in your API docs
beyond the reference information.

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
the generated OpenAPI using the Pecan app described below. The outline itself
is not prescribed since REST APIs vary widely.

Authoring tools
---------------

The API documentation authoring tools are described in the
`Contributor Guide <http://docs.openstack.org/contributor-guide/api-guides.html>`_.

Publishing tools
----------------

The existing OpenStack infrastructure provides publishing to docs.openstack.org
and developer.openstack.org and specs.openstack.org from RST/Sphinx. In the
nova repo, for example, running `tox -e api-ref` builds Sphinx-based API
reference documentation locally.

For publishing OpenAPI-based reference, refer to
https://review.openstack.org/#/c/286659/ as an example that can be used in the
project repo.
