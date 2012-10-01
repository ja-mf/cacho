from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import auth
from django.contrib import admin
admin.autodiscover()

# urls a vistas de otras apps
urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	url(r'^login/$', 'django.contrib.auth.views.login'),
	url(r'^play/', include("cacho_app.urls")),
)

urlpatterns += patterns('cacho_site.views', 
	# login logout
	url(r'^logout/', 'logout_view'),

	# urls de la app.
	url(r'^hello', 'hello'),
	url("", 'index'),
)
