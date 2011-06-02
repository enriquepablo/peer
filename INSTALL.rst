
INSTALL
#######

Development install
+++++++++++++++++++

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

   $ bin/django run_gunicorn
