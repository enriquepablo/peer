
Domain management
=================

Basically, a domain in this system consists of the string representation of
a DNS domain, and a reference to a user, the owner of the domain. It also
has a *verified* mark, the semantics of which will be explained below. Any
user can have any number of domains.

In the user profile view, accessible by clicking on the button labelled with
the username in the upper right corner, there is a link labelled
**add domain**. Following it, the user is presented with a form to add a
new domain. In this form the user simply has to fill in the name of the
domain, and click on the *add domain* button.  After adding a domain the user is
redirected to the verification of the domain.

Adding a domain is not enough to use it in the system. PEER has to verify
that the user has actual management rights over that domain in the DNS
environment. To do this, the user can then click a button labelled *Verify
Ownership* which takes her to the verification page. The verification page shows
2 options: Verify the domain by HTTP or verify it by adding a TXT DNS record.

For the HTTP verification, the user has to create a resource in the root of the
HTTP service for that domain with a specific string given in the verification
page. Once she creates it, she has to click the **Verify ownership by HTTP**
button. The system then sends an HTTP GET request to ``http://<the new
domain>/<the verification string>``, and only when it gets a 200 OK response
code, it considers the domain (and marks it as) verified.

For the DNS verification the user has to create a DNS TXT record in the domain
with that string. Once created, when clicking in **Verify ownership by DNS**,
the system checks that such record exists and only if it exits is the domain
marked as verified. You can also verify a subdomain by adding the TXT record to
the subdomain itself or to the second-level domain.

.. note::

    The DNS record changes may take some time to propagate.

The domains belonging to the user are listed in her profile as
*verified* or *unverified*. In the case of unverified domains she can click on
**Verify Ownership** which takes her to the *verification page*. She can also
delete any domain from this page.

Every entity in PEER is associated with a domain object. This is used in
some validators that check that some parts of the entity's metadata (such as
endpoints) belongs to its entity's domain.
