Instalacion
===========

Construir el ambiente:

Dependencias: redis, pip, virtualenv

	$ git clone git@github.com:jamonardo/cacho.git
	$ cd cacho
	$ virtualenv venv --distribute
	$ source venv/bin/activate
	(venv)$ pip install -r requirements.txt

Iniciar demonio Redis

	$ service redis-server start

Ejecutar servidor (dentro de venv):

	(venv)$ python manage.py runserver_socketio
