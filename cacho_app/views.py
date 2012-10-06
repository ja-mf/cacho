from socketio import socketio_manage

from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from cacho_app.models import GameRoom
from cacho_app.chat_socketio import ChatNamespace

def rooms(request, template="rooms.html"):
    """
    Homepage - lists all rooms.
    """
    context = {"rooms": GameRoom.objects.all()}
    return render(request, template, context)

@login_required
def room(request, slug, template="room.html"):
    """
    Show a room.
    """
    logged_user = request.user.get_full_name()
    context = {"room": get_object_or_404(GameRoom, slug=slug), "user": logged_user}
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
