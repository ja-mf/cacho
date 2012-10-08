from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


@login_required
def index(request):
	return HttpResponse('this is index. welcome ' + request.user.username)
	#return HttpResponseRedirect('/play/')

def logout_view(request):
	logout(request)
	HttpResponse("Logged out!")
	return HttpResponseRedirect('/login/')

def new_user(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/login/')
	else:
		form = UserCreationForm()
	
	return render(request, 'new_user.html', {
		'form': form,
	})

@login_required
def hello(request):
	return HttpResponse('hellow newmann')
