.. _install:

Installation (production)
=========================

This file gives a broad description of the necessary steps to install wger on a
production environment with apache as a webserver. Since this is a regular
django application, refer to its documentation if your setup differs. For a
developemt setup refer to :doc:`development`

The application is compatible and regularly tested with

* sqlite, postgres
* python 2.7, 3.3 and 3.4



Databasse
---------

postgreSQL
~~~~~~~~~~

Install the postgres server and create a database and a user::

    createdb wger
    psql wger
    CREATE USER wger;
    GRANT ALL PRIVILEGES ON DATABASE wger to wger;


sqlite
~~~~~~

No further steps necessary.


Apache
------

Install apache and the WSGI module::

  sudo apt-get install apache2 libapache2-mod-wsgi
  sudo vim /etc/apache2/apache2.conf


Configure apache to serve the application::

  >>>
  WSGIScriptAlias / /home/myuser/wger/wger/wsgi.py
  WSGIPythonPath /home/myuser/wger:/home/myuser/venv-wger/lib/python2.7/site-packages

  <Directory /home/myuser/wger>
      <Files wsgi.py>
          Require all granted
      </Files>
  </Directory>


  <VirtualHost *:80>
      Alias /static/ /home/myuser/static/
      <Directory /home/myuser/static>
          Require all granted
      </Directory>

      Alias /media/ /home/myuser/media/
      <Directory /path/to/mysite.com/media>
          Require all granted
      </Directory>
      ... # Log files, etc.
  </VirtualHost>



Application
-----------

Install the necessary packages to create a virtualenv for python (note that you
might need to install more if you want the thumbnailer to be able to support
more image formats, consult the documentation for pillow for more details)::

  sudo apt-get install git python-dev python-virtualenv
  virtualenv venv-wger
  source venv-wger/bin/activate

If using sqlite, create a folder for it (must be writable by the apache user
so you can just give it the folder with chown):: 

  mkdir db
  chmod o+w db
  
  touch db/database.sqlite
  chmod o+w database.sqlite



Create folders to collect all static resources and save uploaded files (must
be readable by the apache process)::

  mkdir static

  mkdir media
  chmod o+w media

Get the application::

  git clone https://github.com/rolandgeider/wger.git
  cd wger
  pip install -r requirements.txt
  python extras/scripts/create_local_settings.py

Edit your ``settings.py`` file and set the database, ``SITE_URL``,
``STATIC_ROOT`` and ``MEDIA_ROOT``::


      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': u'/home/myuser/db/database.sqlite',
          'USER': '',
          'PASSWORD': '',
          'HOST': '',
          'PORT': '',
      }
  }

  >>> SITE_URL anpassen
  >>> STATIC_ROOT = '/home/myuser/static'
  >>> MEDIA_ROOT = '/home/myuser/wger/media'

Run the installation scritpt, this will load all initial data (exit after it
is done and tries to start a web browser)::

  python start.py


Start.py will create a default administator user (you probably want to change
the password as soon as you log in):

* **username**: admin
* **password**: admin

Collect all static resources:: 

  python manage.py collectstatic
