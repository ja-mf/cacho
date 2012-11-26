Instalacion
===========

Construir el ambiente:

Dependencias: cython, python-2.7, redis

	$ git clone git@github.com:jamonardo/cacho.git
	$ python bootstrap.py
	$ ./bin/buildout
	$ ./bin/django syncdb

Iniciar demonio Redis

	$ service redis-server start

Ejecutar servidor:

	$ ./bin/django runserver_socketio
