from django.conf.urls.defaults import patterns, include, url
import cacho_app.views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	 url(r'^logout/', cacho_app.views.logout_view),
	 url(r'^admin/', include(admin.site.urls)),
	 url(r'^accounts/login/$', 'django.contrib.auth.views.login'),

	# agregar las urls de la app
	url(r'play/', include('cacho_app.urls'))
)
