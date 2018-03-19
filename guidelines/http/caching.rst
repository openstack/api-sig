HTTP Caching and Proxy Behavior
===============================

HTTP was designed to be proxied and cached heavily. HTTP caching by
both intermediary proxies, and by clients themselves, is to be
expected in all cases where it is allowed. This is a fundamental
design point to allow HTTP to work at high scale.

That means that whenever a response is defined as cacheable, for any
reason, the server implementation should assume that those responses
will be cached. This could mean that the server **will never see**
follow up requests if it does not specify appropriate Cache-Control
directives on cacheable responses.

The following HTTP methods are defined as cacheable: HEAD, GET, and
POST :rfc:`7231#section-4.2.3` (section 4.2.3).

Requests that return a status code of any of the following are defined
as cacheable: 200, 203, 204, 206, 300, 301, 404, 405, 410, 414, and
501 :rfc:`7231#section-6.1` (section 6.1).

A common misconception is that requests issued over a secure HTTP connection
are not cached for security reasons. In fact, there is no exception made for
https in the HTTP specification, caching works in exactly the same way as for
non-encrypted HTTP. Most modern browsers apply the same caching algorithm to
secure connections.

Most Python HTTP client libraries are extremely conservative on
caching, so a whole class of completely valid RFC caching won't be
seen when using these clients. Assuming "it works in the Python
toolchain" does not mean that it will in all cases, or is the only way
to implement the HTTP. We expect that in-browser javascript clients
will have vastly different cache semantics (that are completely valid
by the RFC) than the existing Python clients.

Thinking carefully about cache semantics when implementing anything
in the OpenStack API is critical to the API being compatible with the
vast range of runtimes, programming languages, and proxy servers (open
and commercial) that exist in the wild.
