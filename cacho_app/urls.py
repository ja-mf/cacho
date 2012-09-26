from django.conf.urls.defaults import patterns, include, url
import socketio.sdjango

urlpatterns = patterns("chat_app.views",
	url('', index),
	url('^socket\.io', include(socketio.sdjango.urls)),
	url('$', rooms, name='rooms'),
	url('create/$', create, name='create'),
	url('^(?P<slug>.*)$', room, name='room'),
)
