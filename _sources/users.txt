
User authentication and authorization
=====================================

Registration
------------

An unidentified (anonymous) user of the site is always (in every page of the site) presented with 2 links, labelled "Sign up" and "Sign in".

The `Sign up <TERENAPEERDOMAIN/account/register/>`_ link leads the user to a registration form. In this form, the user has to fill in a username, an email address, a password, and a captcha (from `recaptcha <http://www.google.com/recaptcha>`_). All fields are required. The username is validated to ensure that it is unique within the system, and obviously the captcha is also validated.

Once the user submits a valid registration form, the system sends an email to the address entered in the form, containing a link to a confirmation page within the site. Only when the user follows this link and visits the confirmation page, is her account activated.

Authentication
--------------

If a user has an active account on the site, she can log in to the site, following the `Sign in <TERENAPEERDOMAIN/account/login/>`_ link mentioned above and filling in her username and password in the presented form. Once identified, the "Sign up" and "Sign in" links dissapear, and are replaced by one labelled "Logout" and another labelled with the user's full name (or username if the full name is not available). Following the `Logout <TERENAPEERDOMAIN/account/logout/>`_ link invalidates the authentication tokens produced through signing in, so that the user becomes anonymous once again.

User profile
------------

The identified user can follow the link labelled with her name, to edit her user profile. In the presented form, she can change her email and her password, and can also enter a first and a last name. Her full name is a combination of her first and last names.

Authorization
-------------

There are 3 types of users in the system: administrators, regular users, and anonymous users. Administrators are authorized to do anything that the other 2 types of users are, and regular users can do anything that an anonymous user can (except, of course, signing up).

 * Administrator users. Users of this type can access the `django admin interface <TERENAPEERDOMAIN/admin/>`_, and through this interface they can manage other users' accounts (create, modify and delete them). Administrators can also create entities and assign another user as its owner.
 * Regular users. These users can create entities, of which they become owners. They can also assign ownership of their own entities to another user (thereby relinquishing ownership themselves), and delegate management of their entities to (sets of) other users. An entity can only have one owner, that can delegate the management of it to any number of other users.
 * Anonymous users. These users can retrieve entities (there are no private entities).

So, to modify or remove an entity, a user has to be either its owner, an administrator, or a delegate manager for it. Anybody can retrieve entities.
