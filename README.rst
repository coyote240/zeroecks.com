zeroecks.com
============

Source code for https://zeroecks.com

installation
------------

To do a basic installation of the web application, download the latest release
tarball and install it using pip:

    pip install zeroecks.com-<version>.tar.gz

If you are developing locally, create a virtual environment running a minimum
python version of 3.4 and install using the setup script:

    python setup.py develop

This web application is based upon the Tornado web server found at
http://tornadoweb.org and depends upon the tornadobase boilerplat found at
https://github.com/coyote240/tornadobase.  Documentation for those packages
may be found at their respective websites.

configuration
-------------

Configuration options may be passed to the application by command-line or in a
config file specified at run time:

    zeroecks --config=config.py

The config file is simply python and is documented with the Tornado web server.
In addition to those configuration options provided by Tornado, a number of
options have been established:

* dbname - the name of the PostgreSQL database you are using
* dbuser - database user
* dbpass - database user's password
* session_timeout - the timeout, in seconds, before user sessions expire.  Defaults to 86400 (1 day)

The config file may live in any location appropriate to your platform.

load balancer
~~~~~~~~~~~~~

This web application may run behind any HTTP load balancer, though it has only
been tested using nginx.  A basic, introductory nginx configuration has been
included with the package tarball.

database
~~~~~~~~

zeroecks.com depends upon the PostgreSQL database.  Database name, user and
password may be specified in the config file as specified above.

sessions
~~~~~~~~

User web sessions are provided using the Redis database.  A simple default
configuration has been added to the conf directory.

debug mode
~~~~~~~~~~

running the server
------------------

    zeroecks --config=config.py
