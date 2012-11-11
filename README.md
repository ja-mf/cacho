Instalacion
===========

Construir el ambiente:

Dependencias: cython y python-2.7

	$ git clone git@github.com:jamonardo/cacho.git
	$ python bootstrap.py
	$ ./bin/buildout
	$ ./bin/django syncdb

Ejecutar servidor:

	$ ./bin/django runserver_socketio
