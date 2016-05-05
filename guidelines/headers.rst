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

Avoid Proliferating Headers
---------------------------

It can be tempting to use the names of headers as a way of passing
specific information between the client and the server. Where possible
this should be avoided in favor of using a more generic header name
and placing the specifics in the value. For example compare the
following two headers::

  OpenStack-API-Version: compute 2.1
  OpenStack-Nova-API-Version: 2.1

.. note:: The first header is the recommended form. The second header
   is in the form of a microversion header currently in use. It
   effectively demonstrates the problem. Also note that whereas the
   second header uses a service name, the first header uses the more
   correct service type.

At first glance these header name and value pairs convey the same
information, with the second option being a bit easier to parse on
the server side. However consider the following problems when using
the second form:

* A new header is needed every time there is a new service.
* It violates the principle that in key-value based data structures
  the key should be an accessor only, that is: It should be opaque
  and generic.
* If CORS [1]_ middleware is being used, it needs to be configured to
  allow a multitude of headers instead of a generic one.
* Generic library code (in either the client or the server) that is
  supposed to deal with this class of header has to construct or parse
  strings on both sides of the name-value pair.

.. [1] https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS
