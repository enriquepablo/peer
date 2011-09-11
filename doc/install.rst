Installation
============

In this part two types of installation will be covered: the standard one
aimed for production and the development one, which target audience is
the developer community.

After these steps you should have a PEER instance up and running but
please note that many configuration defaults will not be good for your
installation. It is recommended to read the Configuration chapter
right after this one.

Standard installation
---------------------

The standard installation is recommended for having a glimpse at the PEER
application and also for real production deployment.


Creating a virtualenv
~~~~~~~~~~~~~~~~~~~~~

Installing PEER and its dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Creating the database
~~~~~~~~~~~~~~~~~~~~~

The PEER application uses two types of storage:

- A VCS system to store entities metadata. Right now only Git is supported
  but the interface is abstract enough to support other backends.
- A relational database to store domains, users and other information
  besides the entities themselves.

PEER creates the repository where it stores the entities metadata
automatically so you do not need to setup anything. However the relational
database needs to be created and configured manually.

Being a Django project, the PEER application support several different types
of SQL databases such as Postgresql, Mysql, Sqlite, Oracle, etc.

In this documentation we will cover the installation with a Postgresql
database because it is the RDMS we recommend. Check the
`Django documentation`_ to learn how to configure other database backends.

.. _`Django documentation`: http://docs.djangoproject.com/

The first step is to install database server. It is recommended to use the
packages for your Linux distribution:

.. code-block:: bash

  # Fedora example:
  $ yum install postgresql postgresql-server postgresql-libs

  # Debian/Ubuntu example:
  $ apt-get install postgresql postgresql-client

Check your distribution documentation if you do not use neither Fedora nor
Ubuntu.

Now a database user and the database itself must be created. The easiest way
to do this is to login as the postgres system user and creating the user
with that account:

.. code-block:: bash

  $ su - postgres
  $ createuser peer --no-createrole --no-createdb --no-superuser -P
  Enter password for new role: *****
  Enter it again: *****
  $ createdb -E UTF8 --owner=peer peer

With the previous commands we have created a database called *peer* and a
user, which owns the database, called also *peer*. When creating the user
the createuser command ask for a password. You should remember this password
in a later stage of the installation/configuration process.

Now we need to configure Postgresql to accept database connections from the
*peer* user into the *peer* database. To do so, we need to add the following
directive in the pg_hba.conf file:

.. code-block:: bash

  # TYPE   DATABASE    USER       CIDR-ADDRESS        METHOD
  local    peer        peer                           md5

And restart the Postgresql server to reload its configuration:

.. code-block:: bash

  $ service postgresql restart

.. note::
  The location of the pg_hba.conf file depends on your Linux distribution. On
  Fedora it is located at /var/lib/pgsql/data/pg_hba.conf but in Ubuntu it is
  located at /etc/postgresql/8.1/main/pg_hba.conf being 8.1 the version of
  Postgresql you have installed.

To check that everything is correct you shoul try to connect to the *peer*
database using the *peer* user and the password you assigned to it:

.. code-block:: bash

  $ psql -U peer -W peer
  Password for user peer:
  psql (9.0.4)
  Type "help" for help.

  peer=#

.. note::
  We have deliberately keep this postgresql installation super simple since
  we want to focus in the PEER software. If you are serious about puting
  this into production you may consider checking other Postgresql
  configuration settings to improve its performance and security.


Configuring the web server
~~~~~~~~~~~~~~~~~~~~~~~~~~
- Permissions

Development installation
------------------------

 * Previous requirements of the machine:

   $ sudo apt-get install libxml2-dev libxml2
   $ sudo apt-get install libxslt1-dev libxslt1.1

 * Download the code (rw) from github, substituting <username> with your github username::

   $ git clone https://<username>@github.com/Yaco-Sistemas/peer.git

 * Create a virtualenv and activate it, and execute the buildout in it::

   $ cd peer
   $ virtualenv --no-site-packages --python=python2.6 .
   $ source bin/activate
   $ python bootstrap.py
   $ bin/buildout

 * Create the postgresql database and populate it::

   $ sudo su - postgres
   $ createuser peer
   $ createdb -E UTF8 --owner=peer peer
   $ exit
   $ bin/django syncdb --migrate

 * Start the server::

   $ bin/django runserver

'''Note:''' The (system) user that own the apache proccesses must have write permission on the
<buildout_dir>/peer/peer/media/ directory, where the versions repository is placed.
