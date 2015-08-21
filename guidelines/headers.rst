..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode
.. _headers:

======================
HTTP Header Guidelines
======================

Deprecated X-Foo Naming Scheme
------------------------------

In :rfc:`6648` the recommendation to prefix application-specific headers with
``X-`` was retracted. It is mentioned in :rfc:`2616` as a permanently-reserved
prefix for implementors, but is deprecated due to the complexities of migrating
prefixed headers to standardized ones. This has resulted in some standards
reserving X-prefixed names in addition to their non-prefixed headers. (see
X-Archived-At/Archived-At) In the more recent :rfc:`7231#section-8.3.1`
designers of new protocols are discouraged from using X-prefixed headers and to
keep new headers short where possible.

Guidance
********
This **does not** mean it is recommended to replace existing uses of ``X-``, or
in using ``X-`` in private/local/development contexts. New APIs (or new API
features) should make their best effort to not use header names that conflict
with other applications. To do this, use "OpenStack" and the service name in
the header. An example might be "OpenStack-Compute-FooBar", which is unlikely
to be standardized already or conflict with existing headers.

:rfc:`6648` intentionally does not disallow using ``X-`` as a prefix, but does
remove the experimental/unstandardized semantics from the prefix. For
existing projects, it is acceptable to create new headers prefixed with X
since it is likely that the rest of the headers already standardized in the API
begin with ``X-``.

Examples
********

Some good header names that are clear, unlikely to conflict, and could become
standardized might be ``OpenStack-Identity-Status`` Some headers that are at
risk for conflicts might look like::

  Account-ID
  Host-Name
  Storage-Policy

In these cases, adding ``OpenStack-`` as a prefix resolves the ambiguity, as
in::

  OpenStack-Identity-Account-ID
  OpenStack-Networking-Host-Name
  OpenStack-Object-Storage-Policy
