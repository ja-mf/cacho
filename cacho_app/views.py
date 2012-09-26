from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout

from socketio import socketio_manage

# importar modelos de la app si es que hay (y se ocupan)

# falta crear modulo cacho_socketio.py, el cual contendra
# funciones que manipularan la interaccion con socketio
# es decir, conectores a un modulo de logica de juego, 
# envio y recepcion de mensajes de chat.
# ver django_chat.
#
# from cacho_app.cacho_socketio import ChatNamespace

@login_required
def index(request):
	return HttpResponse(request.user.get_full_name())

def logout_view(request):
	logout(request)
	HttpResponse("Logged out!")
	return HttpResponseRedirect('/game/')

def rooms(request):
	return HttpResponse('room list')

def room(request):
	return HttpResponse('one room')

def create(request):
	return HttpResponse('on POST a room')
