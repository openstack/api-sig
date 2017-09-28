Cross-Project Liaisons
======================

Description
-----------

The API Special Interest Group seeks API subject matter experts for each
project to communicate plans for API updates, review API guidelines with their
project's view in mind, and review the API Special Interest Group guidelines as
they are drafted.  The Cross-Project Liaison (CPL) should be familiar with the
project's REST API design and future planning for changes to it.

* The liaison should be the PTL or whomever they delegate to be their
  representative
* The liaison is the first line of contact for the API Special Interest Group
  team members
* The liaison may further delegate work to other subject matter experts
* The liaison should be aware of and engaged in the API Special Interest Group
  `Communication channels
  <https://wiki.openstack.org/wiki/API_Working_Group#Communication>`_
* The Nova team has been very explicit about how they will liaise with the
  API Special Interest Group; see the `Responsibilities of Liaisons <https://wiki.openstack.org/wiki/Nova/APIWGLiaisons>`_

Tooling
-------

To make it easier to engage the liaisons, we have a tool that will add all
current liaisons to an API WG review.

You can run the tool like so from the base dir of the api-wg repository.

::

    $ python3 tools/add-reviewers.py my-gerrit-username 183599
    Added 21 reviewers to 183599

To get help use ``--help``.

::

    $ python3 tools/add-reviewers.py --help

Liaisons
--------

.. literalinclude:: liaisons.json
   :language: json
