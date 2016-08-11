.. _links:

Links
=====

Links to other resources often need to be represented in responses. There is
already a well established format for this representation in `JSON
Hyper-Schema: Hypertext definitions for JSON Schema
<http://json-schema.org/latest/json-schema-hypermedia.html>`_.
This is already the `prevailing representation
<https://wiki.openstack.org/wiki/API_Working_Group/Current_Design/Links>`_ in
use by a number of prominent OpenStack projects and also in use by the
:ref:`errors` guideline.

.. note:: Before inventing a new value for ``rel``, please check the existing
   `Link Relations
   <http://www.iana.org/assignments/link-relations/link-relations.xhtml>`_ for
   something you can reuse.

Links Example
-------------

    .. code-block:: javascript

        {
          "links": [
            {
              "rel": "help",
              "href": "http://developer.openstack.org/api-ref/compute/#create-server"
            }
          ]
        }
