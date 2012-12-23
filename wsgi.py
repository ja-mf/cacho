from re import match
from thread import start_new_thread
from time import sleep
from os import getpid, kill, environ
from signal import SIGINT

from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler
from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands.runserver import naiveip_re, DEFAULT_PORT
from django.utils.autoreload import code_changed, restart_with_reloader
from socketio.server import SocketIOServer

RELOAD = False

def reload_watcher():
    global RELOAD
    while True:
        RELOAD = code_changed()
        if RELOAD:
            kill(getpid(), SIGINT)
        sleep(1)

addr = '127.0.0.1'
port = 8000

environ["DJANGO_SOCKETIO_PORT"] = str(port)
environ["DJANGO_SETTINGS_MODULE"] = 'cacho_site.settings'

bind = (addr, port)

da_server = WSGIHandler()


