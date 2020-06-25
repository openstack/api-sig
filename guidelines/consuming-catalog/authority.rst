Consuming Service Types Authority
=================================

The `OpenStack Service Types Authority`_ is data about official service type
names and historical service type names commonly in use from before there was
an official list. It is made available to allow libraries and other client
API consumers to be able to provide a consistent interface based on the
official list but still support existing names. Providing this support is
highly recommended, but is ultimately optional. The first step in the matching
process is always to return direct matches between the catalog and the user
request, so the existing consumption models from before the existence of the
authority should always work.

In order to consume the information in the `OpenStack Service Types Authority`_
it is important to know a few things:

#. The data is maintained in YAML format in git. This is the ultimately
   authoritative source code for the list.

#. The data is published in JSON format at
   https://service-types.openstack.org/service-types.json and has a JSONSchema
   at https://service-types.openstack.org/published-schema.json.

#. The published data contains a version which is date based in
   `ISO Date Time Format`_, a sha which contains the git sha of the
   commit the published data was built from, and pre-built forward and reverse
   mappings between official types and aliases.

#. The JSON file is served with ETag support and should be considered highly
   cacheable.

#. The current version of the JSON file should always be the preferred file to
   use.

#. The JSON file is similar to timezone data. It should not be considered
   versioned such that stable releases of distros should provide a
   frozen version of it. Distro packages should instead update for all
   active releases when a new version of the file is published.


.. _OpenStack Service Types Authority: https://opendev.org/openstack/service-types-authority/
.. _ISO Date Time Format: https://tools.ietf.org/html/rfc3339#section-5.6
