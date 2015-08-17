=========================================
Process for adding or changing guidelines
=========================================

This document describes the process we will use before merging a non
trivial changeset in the guidelines directory. A non trivial changeset
is one which is more than a spelling/grammar typo or reformatting
change.

The guidelines are initially intended to be a working group draft
document. Our intent is to move fairly quickly to get published draft
guidelines so this process reflects a preference for efficiency while
gathering consensus.

Review process
--------------

The following process should occur:

1. Minor typo/formatting change updates do not have any minimum time
   that they must be proposed before merging. They must have at least
   one +1 vote other than the approver and no -1.

2. A changeset which adds a new guideline or makes a substantial change
   to an existing guideline must reach consensus within the API Working
   Group (WG).

   In the guideline review, consensus means the changeset must be available
   for review in its near final form for at least 2 working days. Minor
   typo/formatting change updates do not reset the counter. There must be at
   least four +1 votes and no -1's unless the concern by the -1 vote has been
   discussed in an API WG meeting. Once the matter has been discussed there
   should be no more than 20% (of votes cast) -1 votes.

   Note that discussion on Gerrit should be encouraged as the first
   response and summaries from discussions on IRC meetings should be
   summarised back to Gerrit for those who can't attend the
   meetings. However we recognise that sometimes higher bandwidth, low
   latency discussions can help break deadlocks.

3. Once a changeset meets the requirements of #2, the :doc:`liaisons`
   (CPLs) for the API WG should be engaged on various channels.

   1. Review. The CPLs must be added as reviewers to any changeset that has
   reached consensus by the API WG. You can use the ``add-reviewers.py``
   script to do this, see :doc:`liaisons` for more information.

   2. The openstack-dev mailing list. An email must be sent to the
   openstack-dev mailing list with the subject "[all][api] New API
   Guidelines Ready for Cross Project Review". The email will contain links
   to all of the guidelines that have reached consensus.

   3. The `Cross Project Meeting
   <https://wiki.openstack.org/wiki/Meetings/CrossProjectMeeting>`_. An
   agenda item should be added to the Cross Project Meeting which
   reads "New API Guidelines ready for cross project review" followed by a
   link to the email above from the `openstack-dev archives
   <http://lists.openstack.org/pipermail/openstack-dev/>`_. The Cross Project
   Meeting should be attended by an API WG member to highlight the agenda
   item.

4. Once a changeset meets the requirements of #3, it should be frozen by
   exactly one core reviewer by setting Code-Review +2. Only the core reviewer
   responsible for freezing the guideline should +2 it. All other core
   reviewers should vote with at most a +1 when reviewing.

5. Once a changeset meets the requirements of #4, the CPLs have 1 week to
   review it. If there is no review by a CPL, lazy consensus is assumed.
   If there is a -1 review by a CPL that requires an update to the changeset,
   it does not reset the 1 week the CPLs have to review it.

6. Once a changeset meets the requirements of #5, it can be merged.

   An email should be sent to the openstack-dev mailing list containing the
   links to all of the guidelines that have been merged. This could
   simply be a reply to the original email in #3.2. The finalized
   guidelines should be buffered such that a maximum of one announcement
   email is sent per week.

7. Anyone who is listed on the `API Working Group Wiki
   <https://wiki.openstack.org/wiki/API_Working_Group>`_ by
   25/5/2015 (L1) can vote during the Liberty development cycle.

8. Before an official version of the guidelines can be released the
   following has to occur:

   * An 80% (of votes cast) majority vote on the document as a whole
     with one vote per OpenStack PTL (or delegate).

   * Reviewed and approved by the TC. We are a delegated group from
     the TC so they ultimately get final say on what we are able to
     release.

Proposing a new guideline
-------------------------

When proposing a new guideline you should start by using the
:doc:`guideline template <template>` to generate the basic
structure. Copy the ``template.rst`` file to the ``guidelines`` directory
with a filename reflecting your new guideline (for example
``guidelines/errors.rst``), and then follow the instructions within the
template. Once complete you should follow the `developer workflow`_ and
the previously stated review process to have your guideline accepted.

.. _developer workflow: http://docs.openstack.org/infra/manual/developers.html
