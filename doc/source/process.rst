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

For trivial changes (as defined above) there is no minimum time that
they must be proposed before merging. They must have at least one +1
vote other than the approver and no -1. Once this is true a working
group core may merge the change.

For changes which add a new guideline or make substantial changes to
an existing guideline reaching consensus is an explicit goal. To
that end there is a well defined process to ensure that proposals
receive adequate review by the working group, cross project
liaisons, and the OpenStack community at large.

In the various stages of the review process (defined below) consensus
means the changeset is in its near final form for at least two working
days. Minor typo/formatting changes do not reset the counter. There
must be at least four +1 votes and no -1 votes unless the concern
related to the -1 vote has been discussed in an API WG meeting. Once
the matter has been discussed there should be no more than 20% of
votes cast as -1 votes.

Discussion on Gerrit should be encouraged as the primary response.
When discussion on IRC (in meetings or otherwise) is required that
discussion should be summarized back to Gerrit.

That process is:

1. Working group members should review proposed guideline changes
   and reach consensus.

2. When consensus is reached within the group the guideline should
   be marked as *frozen* and cross project liaisons (CPLs) should
   be invited to review the guideline. There is an ``add-reviewers.py``
   script to do this. See :doc:`liaisons` for more information.

   A proposal can be frozen by exactly one core reviewer by setting
   Code-Review +2. Only the core reviewer responsible for freezing the
   proposal should +2 it. All other core reviewers should vote with at
   most a +1 when reviewing.

3. The CPLs have one week to review the proposal. If there are no
   reviews lazy consensus is assumed. If there is a -1 review by a CPL
   that requires an update to the changeset, it does not reset the 1
   week the CPLs have to review it.

4. When there is consensus from the CPLs, the proposal may be
   merged.

   An email should be sent to the openstack-dev mailing list containing
   the links to all of the guidelines that have recently merged. The
   finalized guidelines should be buffered such that a maximum of one
   announcement email is sent per week.

If at any time during this process there is difficulty reaching
consensus or an apparent lack of information or input, additional
input should be sought from the rest of the community. Two ways to
do this include (preferring email):

1. The openstack-dev mailing list. An email may be sent to the
   openstack-dev mailing list with the subject "[all][api] New API
   Guidelines Ready for Cross Project Review". The email should contain
   links to the guidelines that need additional input.

2. The `Cross Project Meeting
   <https://wiki.openstack.org/wiki/Meetings/CrossProjectMeeting>`_. An
   agenda item should be added to the Cross Project Meeting which
   indicates need for discussion. Links to the guidelines that need
   additional input should be provided. When this is done an API WG
   member must attend the meeting to highlight the agenda item.

Merged guidelines comprise a draft of the official guidelines. Before
an official version of the guidelines can be released the following
has to occur:

* An 80% (of votes cast) majority vote on the document as a whole
  with one vote per OpenStack PTL (or delegate).

* Reviewed and approved by the TC. The API WG is a delegated group from
  the TC so the TC ultimately get final say on what the working
  group are able to release.

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
