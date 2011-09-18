Configuration
=============

In this section you will learn how to configure your PEER instance. As any
Django project all configuration options are stored in a *settings.py* file,
which is located inside the main PEER directory.

However it is not recommended to change the *settings.py* file directly since
that would make upgrades more difficult for you. You should see this file
as the file with the **default** configuration settings. You should put
your own settings in a file called *local_settings.py*. The options you
put there will override the same options located in the *settings.py* file.

First we will cover the options that you **must** change in order to run
the PEER instance correctly. Then we will see other optional settings that
you may want to change but that are ok with their default values. At the
end of this section you will see *local_settings.py* example.

If you change any setting you must restart your web server in order to
see your new settings applied.

Settings you should change
--------------------------

Database settings
~~~~~~~~~~~~~~~~~

Here you tell PEER the necessary information to connect to your database. The
default values will not probably fit your case:

.. code-block:: python

 DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'NAME': 'peer',
         'USER': 'peer',
         'PASSWORD': 'peer',
         'HOST': '',
         'PORT': '',
     }
 }

This option is pretty much self explanatory. Check the Django documentation
to learn all the details about this setting.

The Site object
~~~~~~~~~~~~~~~

Django uses a Site model to store information about the domain your project
is running at. This is used when composing links that are not shown in the
web application itself, such as links in the emails that are sent.

So you need to log in as the administrator user and go to the `Django admin
interface`_ to edit the only Site object you should have:

.. _`Django admin interface`: http://127.0.0.1:8000/admin/

.. figure:: _static/change-site-object.png

It is very important to enter the correct Domain name so users will be able
to complete the registration process by clicking in correct links in their
inboxes.

.. note::
  The id of your Site object should match the value of the SITE_ID setting.
  You shouldn't need to do anything special here since this is the default
  behaviour.

Mail settings
~~~~~~~~~~~~~

The PEER instance needs to send email in order to correctly perform several
actions such as sending registration activation links or warning users when
their metadata is about to expire.

The *DEFAULT_FROM_EMAIL* settings is used as the *From* header in all these
emails:

.. code-block:: python

 DEFAULT_FROM_EMAIL = 'no-reply@example.com'

You will probably want to change this email address to fit the subdomain
where you installed the PEER instance.

The next settings define where is your SMTP server and how to connect to it:

.. code-block:: python

 EMAIL_HOST = 'smtp.example.com'
 EMAIL_PORT = 25

.. note::
  You can check Django settings reference if your SMTP server require
  authentication.

Recaptcha keys and the Django SECRET_KEY
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PEER uses the Recaptcha service to prevent spammers to register into your
PEER instance. In order to use such service you should register your PEER
site into Recaptcha and they will give you a public and a private key. You
have to write these keys in your *local_settings.py* file:

.. code-block:: python

 RECAPTCHA_PUBLIC_KEY = ''
 RECAPTCHA_PRIVATE_KEY = ''

As you can see the default values for these options are empty so you must
not skip this step if you want the user registration to operate correctly.

Django uses another key for some features. This key is called the
*SECRET_KEY* and should be unique. When a new Django project is created the
django-admin.py program will create such a key for you but the PEER project
is already cloned so you will need to create it yourself. One way to create
such a key is executing the following command:

.. code-block:: bash

 python -c "from random import choice; print ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789\!@#$%^&*(-_=+)') for i in range(50)])"

And now paste it into the SECRET_KEY option:

.. code-block:: python

 SECRET_KEY = ''

As before, the default value of the SECRET_KEY is empty for security reasons.

MEDIA_ROOT setting
~~~~~~~~~~~~~~~~~~

This settings specifies a directory where user files will be stored. In PEER,
this directory contains the main metadata repository, usually stored as a
GIT repository.

.. code-block:: python

 MEDIA_ROOT = os.path.join(BASEDIR, 'media')

By default the *MEDIA_ROOT* root lives inside the PEER main directory which
is **not** what you usually want. You really want to put this directory
outside your PEER main directory in order to prevent data lost when
upgrading the PEER software. Actually the upgrade process does not lost any
data but as the new version is installed into another directory you will
need to move the media root or change the MEDIA_ROOT setting anytime you
upgrade PEER.

Also, remember that the user that your web server is run as needs to have
write access to the *MEDIA_ROOT* directory.

Terms of use texts
~~~~~~~~~~~~~~~~~~

PEER asks the user to accept some terms of use in two situations:

- When the user is registered in the site.
- When the user import metadata from his computer or a remote location.

In both cases a legal text should be presented to the user in order to
prevent future complications. These text must be stored in UTF-8 encoded
text files and you will configure their locations with a couple of settings:

.. code-block:: python

 USER_REGISTER_TERMS_OF_USE = os.path.join(BASEDIR, 'user_register_terms_of_use.txt')
 METADATA_IMPORT_TERMS_OF_USE = os.path.join(BASEDIR, 'metadata_import_terms_of_use.txt')

The default values reference a couple of files located inside the PEER main
directory. The content of these files is not very useful skeaking about legal
terms, so you should contact your lawyers and create your own files. As with
the `MEDIA_ROOT setting`_, it is recommended to place these files outside
the PEER main directory to make upgrades easier.

Settings you may change
-----------------------

Theme
~~~~~

PEER look can be customizable by changing the PEER_THEME setting:

.. code-block:: python

 PEER_THEME = {
     'LINK_COLOR': '#5669CE',
     'LINK_HOVER': '#1631BC',
     'HEADING_COLOR': '#1631BC',
     'INDEX_HEADING_COLOR': '#ff7b33',
     'HEADER_BACKGROUND': '',
     'CONTENT_BACKGROUND': '',
     'FOOTER_BACKGROUND': '',
     'HOME_TITLE': 'Nice to meet you!!',
     'HOME_SUBTITLE': 'Say hello to federated worldwide services',
     'JQUERY_UI_THEME': 'default-theme',
 }

Each element of this dictionary has its own purpose:

LINK_COLOR
 Foreground color for the links.

LINK_HOVER
 Foreground color for he links when the mouse cursor is over hem.

HEADING_COLOR:
 Foreground color for the heading section.

INDEX_HEADING_COLOR:
 Foreground color for the heading section of the index page (homepage).

HEADER_BACKGROUND:
 Background color for the header section.

CONTENT_BACKGROUND:
 Background color for the content section.

HOME_TITLE:
 Text that will be shown in the main banner of the homepage.

HOME_SUBTITLE:
 Secondary text that will be shown in the main banner of the homepage.

JQUERY_UI_THEME:
 jQuery UI theme to use. You can generate these themes using the `Theme
 Roller application`_. Then you should put this theme inside the css
 directory. This theme should be for jQuery UI 1.8.14 version. This theme
 will affect the look of every button, icon, user messages and other widgets
 accross the whole site.

.. _`Theme Roller application`: http://jqueryui.com/themeroller/

Check the :doc:`branding` section for more information about how to
create a coherent theme.


Registration settings
~~~~~~~~~~~~~~~~~~~~~

These settings affect the user registration process. Right one only one
setting exists:

.. code-block:: python

 ACCOUNT_ACTIVATION_DAYS = 2

This is the number of days the activation key can be used. After this period,
the user will need to register again.

Metadata Validation
~~~~~~~~~~~~~~~~~~~

The METADATA_VALIDATORS settings specifies the validators that will be used
in the validation process that happens every time an entity's metadata is
changed. It is a list of strings, each string representing the full path
of a python function, that is the validator:

.. code-block:: python

 METADATA_VALIDATORS = (
     'peer.entity.validation.validate_xml_syntax',
     'peer.entity.validation.validate_domain_in_endpoints',
 )

In order to save the changes of an entity's metadata all the validators must
succeeded.

A validator is just a single python function with the following interface:

* It receives two arguments: the entity object and an XML string representing
  the metadata.
* It returns a list of error messages or an empty list if the XML string is
  valid.

Check the provided validators for examples about how to write your own
validators.

SAMLmetaJS plugins
~~~~~~~~~~~~~~~~~~

SAMLmetaJS is a jQuery plugin that turns a simple HTML textarea element into
a full blown SAML metadata editor. It has a small core and several plugins
for editing specific parts of the metadata XML.

With this setting you can set which plugins are going to be active and in
which order. This will affect the tabs that appear in the metadata edition
view.

.. code-block:: python

 SAML_META_JS_PLUGINS = ('info', 'org', 'contact', 'saml2sp', 'certs',
                         'attributes')

Check the `SAMLmetaJS website`_ for a complete list of all available plugins.

.. _`SAMLmetaJS website`: http://samlmetajs.simplesamlphp.org/

Pagination and feeds settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With these settings you can control the number of entities that are
shown in certain circunstances.

The MAX_FEED_ENTRIES setting controls the number of entities that are
returned in the global rss feed.

.. code-block:: python

 MAX_FEED_ENTRIES = 10

If you do not define this setting the global rss feed will return the full
set of entities. Be careful if you have a lot of entities since this can
be degradate performance.

The ENTITIES_PER_PAGE setting controls the number of entities that
are displayed in each page of the full list view and the search results view.

.. code-block:: python

 ENTITIES_PER_PAGE = 10

Expiration warning
~~~~~~~~~~~~~~~~~~

The EXPIRATION_WARNING_TIMEDELTA setting specifies the time threshold that
should be used to determine if a warning email should be sent when the
metadata of an entity is about to expire. If the time when the metadata
is expired minus the EXPIRATION_WARNING_TIMEDELTA is greater than the current
time, a warning email is sent to the entity's team. For example, if the
metadata expires the 17th of September of 2011 at 16:00 and the
EXPIRATION_WARNING_TIMEDELTA is set to 5 hours, that day at 11:00  a warning
email will be sent.

The value of this settings should be a datetime.timedelta object. Check the
`Python documentation`_ for valid units for this object.

.. _`Python documentation`: http://docs.python.org/library/datetime.html#timedelta-objects

.. code-block:: python

 EXPIRATION_WARNING_TIMEDELTA = datetime.timedelta(days=1)

This feature requires that you setup a cron job that calls the
*expirationwarnings* PEER command. Something like this should work:

.. code-block:: bash

 0 * * * * /var/www/peer/bin/django-admin.py expirationwarnings --settings=peer.settings

Administrators
~~~~~~~~~~~~~~

The last setting you may want to change is the ADMINS setting. You put here
the names and emails of the administrator stuff that will run the PEER site.

This is useful because some times emails are sent automatically to these
people, for example, when a crash happens.

.. code-block:: python

 ADMINS = (
     # ('Your Name', 'your_email@example.com'),
 )

.. note::
 This people will not get PEER user accounts automatically. You should create
 them as any other user.

Example local_settings.py file
------------------------------

You can use this fragment as an skeleton file to get you started but remember
that some settings need unique values you must provide yourself.

.. code-block:: python

 DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'NAME': 'peer',
         'USER': 'peer',
         'PASSWORD': 'peer',
         'HOST': '',
         'PORT': '',
     }
 }

 DEFAULT_FROM_EMAIL = 'no-reply@peer.terena.org'
 EMAIL_HOST = 'smtp.terena.org'
 EMAIL_PORT = 25

 # do not use these keys: they are invalid
 RECAPTCHA_PUBLIC_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
 RECAPTCHA_PRIVATE_KEY = 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'

 # do not use this key: create your own
 SECRET_KEY = '0123456789qwertyuiopasdfghjklzxcvbnm'

 MEDIA_ROOT = '/var/peer-media'

 USER_REGISTER_TERMS_OF_USE = '/etc/peer/user_register_terms_of_use.txt'
 METADATA_IMPORT_TERMS_OF_USE = '/etc/peer/metadata_import_terms_of_use.txt'

 PEER_THEME = {
     'LINK_COLOR': '#5669CE',
     'LINK_HOVER': '#1631BC',
     'HEADING_COLOR': '#1631BC',
     'INDEX_HEADING_COLOR': '#ff7b33',
     'HEADER_BACKGROUND': '',
     'CONTENT_BACKGROUND': '',
     'FOOTER_BACKGROUND': '',
     'HOME_TITLE': 'Nice to meet you!!',
     'HOME_SUBTITLE': 'Say hello to federated worldwide services',
     'JQUERY_UI_THEME': 'default-theme',
 }

 METADATA_VALIDATORS = (
     'peer.entity.validation.validate_xml_syntax',
     'peer.entity.validation.validate_domain_in_endpoints',
     'peer.entity.validation.validate_domain_in_entityid',
 )

 SAML_META_JS_PLUGINS = ('info', 'org', 'contact', 'saml2sp', 'certs')

 MAX_FEED_ENTRIES = 100
 ENTITIES_PER_PAGE = 10

 EXPIRATION_WARNING_TIMEDELTA = datetime.timedelta(hours=2)

 ADMINS = (
     # ('Your Name', 'your_email@example.com'),
 )