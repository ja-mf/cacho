from django.conf.urls.defaults import patterns, include, url
import cacho_app.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cachupin.views.home', name='home'),
    # url(r'^cachupin/', include('cachupin.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
	 url(r'^game/', cacho_app.views.index),
    url(r'^admin/', include(admin.site.urls)),
	 url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
)
