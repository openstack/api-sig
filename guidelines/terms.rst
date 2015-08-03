Terms
=====

As Phil Karlson [once said](http://martinfowler.com/bliki/TwoHardThings.html):

> There are only two hard things in Computer Science: cache invalidation and
> naming things.

Over time, various terms and synonyms for those terms generate some
controversy, and different teams end up using different words to reference the
same object or resource. This document serves to record decisions that were
made regarding certain terms, and attempts to succinctly define each term.

* **project** vs. **tenant**

  **project** shall be used to describe the concept of a group of OpenStack
  users that share a common set of quotas. The older term **tenant** should
  *not* be used in OpenStack REST APIs.

* **server** vs. **instance**

  **server** shall be used to describe a virtual machine, a
  bare-metal machine, or a containerized virtual machine that is used
  by OpenStack users for compute purposes. The older term
  **instance** that is also by Amazon Web Services EC2 API to
  describe a virtual machine, should *not* be used in OpenStack REST
  APIs.

* **project name** vs. **service type**

  Most OpenStack projects have both a "project name" (e.g., Nova, Keystone,
  etc.) and a "service type" (e.g., Compute, Identity, etc.). Some REST API
  features (e.g., JSON-Home, API Microversions, etc.) need to expose each
  project in a request/response.
  The project *should* be represented with its **service type** if it has both
  a "project name" and a "service type" because its project name is subject to
  change (e.g., Neutron was Quantum) and its service type is more stable. The
  service type should come from "type" of the corresponding OpenStack Identity
  service catalog entry.
