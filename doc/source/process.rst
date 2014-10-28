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

The following process should occur:

1. Minor typo/formatting change updates do not have any minimum time
   that they must be proposed before merging. They must have at least
   one +1 vote other than the approver and no -1.

2. A changeset which adds a new guideline or to change a guideline
   included during the initial project creation must be available for
   review in in its near final form for at least 2 working days before
   merging. Minor typo/formatting change updates do not reset the
   counter. There must be at least four +1 votes and no -1's unless the
   concern by the -1 vote has been discussed in an API WG
   meeting. Once the matter has been discussed there should be no more
   than 20% (of votes cast) -1 votes before merging.

   Note that discussion on Gerrit should be encouraged as the first
   response and summaries from discussions on IRC meetings should be
   summarised back to Gerrit for those who can't attend the
   meetings. However we recognise that sometimes higher bandwidth, low
   latency discussions can help break deadlocks.

3. A changeset which substantially changes the meaning of an existing
   guideline which has been voted on must be available for review in
   its near final form for at least 3 working days before
   merging. Minor typo/formatting changes do not reset the
   counter. There must be at least four +1 votes and no -1's unless
   the concern by the -1 vote has been addressed in an API WG
   meeting. Once the matter has been discussed there should be no more
   than 20% (of votes cast) -1 votes.

4. Anyone who is listed on the `API Group Wiki
   <https://wiki.openstack.org/wiki/API_Working_Group>`_ by
   18/12/2014 (K1) can vote during the Kilo development cycle.

5. Before an official version of the guidelines can be released the
   following has to occur:

   * An 80% (of votes cast) majority vote on the document as a whole
     with one vote per OpenStack PTL (or delegate).

   * Reviewed and approved by the TC. We are a delegated group from
     the TC so they ultimately get final say on what we are able to
     release.
