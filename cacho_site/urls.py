from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import auth
from django.contrib import admin
import socketio.sdjango
admin.autodiscover()

# urls a vistas de otras apps
urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	url(r'^login/$', 'django.contrib.auth.views.login'),
	url(r'^play/', include("cacho_app.urls")),

	# socket.io
   url("^socket\.io", include(socketio.sdjango.urls)),

	(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes':True}),

)

urlpatterns += patterns('cacho_site.views', 
	# login logout
	url(r'^logout', 'logout_view'),
	url(r'^register', 'new_user'),
	url(r'^reglas', 'rules'),

	# urls de la app.
	url(r'^hello', 'hello'),
	url("", 'index'),
)
