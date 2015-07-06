..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..
 The title of your guideline should replace the
 "Example Guideline Category"

==========================
Example Guideline Category
==========================

Introduction paragraph -- what does this guideline category address? A single
paragraph of prose that implementors can understand. This paragraph should
describe the intent and scope of the guideline. The title and this first
paragraph should be used as the subject line and body of the commit message
respectively.

Some notes about using this template:

* Your guideline should be in ReSTructured text, like this template.

* Please wrap text at 79 columns.

* For help with syntax, see http://sphinx-doc.org/rest.html

* To test out your formatting, build the docs using tox, or see:
  http://rst.ninjs.org

* For help with OpenStack documentation conventions, see
  https://wiki.openstack.org/wiki/Documentation/Conventions

Each file should be a group of related guidelines, such as "HTTP Headers" or
similar. Each guideline gets its own subheader, and within each section there
is an overview/introduction, a guidance section, examples, and references. Not
every guideline will fill in every section. If a section isn't needed for a
particular guideline, delete it if you're **really** sure it's superfluous.

Guideline Name
--------------

A detailed guideline that is being suggested. It should also have an
introduction if applicable.

Guidance
********

The actual guidance that the API working group would like to provide.

* The guideline should provide a clear recitation of the actions to be
  taken by implementors.

* Reference to specific technology implementations (for example,
  XXX-Y.Z package) should be avoided.

* External references should be described by annotations with the
  links to the source material in the References section. (for example,
  please see :rfc:`0000` or this footnote guide [#f1]_)

Examples
********

A series of examples that demonstrate the proper usage of the guideline
being proposed. These examples may include, but are not limited to:

* JSON objects.

* HTTP methods demonstrating requests and responses.

The examples should not include:

* Code samples designed for implementation.

References
**********

References may be provided in cases where they aid in giving a more complete
understanding of the guideline. You are not required to have any references.
Moreover, this guideline should still make sense when your references are
unavailable. Examples of what you could include are:

* Links to mailing list or IRC discussions

* Links to notes from a summit session

* Links to relevant research, if appropriate

RST supports footnotes in the following format:

.. rubric:: Footnotes

.. [#f1] http://sphinx-doc.org/rest.html#footnotes
