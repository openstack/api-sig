Representation Structure Conventions
====================================

Singular resources
------------------

TODO

Collection resources
--------------------

JSON request and response representations for collection resources should be
an object that includes a top-level property to encapsulate the collection of
resources. The value of this property should be a JSON array whose elements are
the JSON representations of the resources in the collection.

For example, when listing networks using the ``GET /networks`` API,

  - The JSON response representation would be structured as follows:

    .. code-block:: javascript

        {
          "networks": [
            {
              // Properties of network #1
            },
            {
              // Properties of network #2
            }
          ]
        }

*Rationale*: Having JSON collection resource representations be an object
— as opposed to an array — allows the representation to be extensible. For
instance, properties that represent collection-level metadata could be
added at a later time.

Here are some other OpenStack APIs that use this structure:

- `Bulk creating networks <http://developer.openstack.org/api-ref-networking-v2.html#networks>`_,
  which uses the top-level ``networks`` property in the JSON request and
  response representations.
- `Listing stacks <http://developer.openstack.org/api-ref-orchestration-v1.html#stacks>`_,
  which uses the top-level ``stacks`` property in the JSON response
  representation.
- `Listing database instances <http://developer.openstack.org/api-ref-databases-v1.html#Database_Instances>`_,
  which uses the top-level ``instances`` property in the JSON response
  representation.
- `Listing servers <http://developer.openstack.org/api-ref-compute-v2.html#compute_servers>`_,
  which uses the top-level ``servers`` property in the JSON response
  representation.
