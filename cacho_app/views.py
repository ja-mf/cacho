from socketio import socketio_manage

from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from cacho_app.models import GameRoom
from cacho_app.cacho_socketio import GameNamespace

import redisutils

@login_required
def rooms(request, template="rooms.html"):
	"""
	Listar todos los rooms y sus participantes
	"""
	
	# hacer el contexto para la vista,
	# armar los objetos room y la lista de jugadores actuales
	r = []
	rooms = GameRoom.objects.all()
	for room in rooms:
		r.append([room, redisutils.get_members_name(room.id)])
	
	context = {"rooms": r}
	return render(request, template, context)

@login_required
def room(request, slug, template="room.html"):
	"""
	Entrar a una sala de juego
	"""
#	logged_user = request.user.get_full_name()
	context = {"room": get_object_or_404(GameRoom, slug=slug)}
	return render(request, template, context)

def create(request):
	"""
	Handles post from the "Add room" form on the homepage, and
	redirects to the new room.
	"""
	name = request.POST.get("name")
	if name:
	    room, created = GameRoom.objects.get_or_create(name=name)
	    return redirect(room)
	return redirect(rooms)
