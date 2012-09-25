from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required
def index(request):
	return HttpResponse(request.user.get_full_name())

def logout_view(request):
	logout(request)
	HttpResponse("Logged out!")
	return HttpResponseRedirect('/game/')

