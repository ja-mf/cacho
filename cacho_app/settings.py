import os
import django

# calculate relative paths to define settings
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

# Django settings for cacho project.
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
	  ('admin', 'user@localhost'),
)

MANAGERS = ADMINS

DATABASES = {
	 'default': {
		  'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
		  'NAME': 'dev.db',							  # Or path to database file if using sqlite3.
		  'USER': '',							  # Not used with sqlite3.
		  'PASSWORD': '',						  # Not used with sqlite3.
		  'HOST': '',							  # Set to empty string for localhost. Not used with sqlite3.
		  'PORT': '',							  # Set to empty string for default. Not used with sqlite3.
	 }
}

TIME_ZONE = 'America/Santiago'
LANGUAGE_CODE = 'es_CL'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

#MEDIA_ROOT = '/home/jamon/utfsm/cacho/media/'
MEDIA_ROOT = os.path.join(SITE_ROOT, 'assets')
MEDIA_URL = 'http://localhost/assets/'

#STATIC_ROOT = '/home/jamon/utfsm/cacho/static/'
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
	 # Put strings here, like "/home/html/static" or "C:/www/django/static".
	 # Always use forward slashes, even on Windows.
	 # Don't forget to use absolute paths, not relative paths.
)

STATICFILES_FINDERS = (
	 'django.contrib.staticfiles.finders.FileSystemFinder',
	 'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#	  'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '2z6p0f2_f14j!8o=usfqi#9^q5egf0+!zyx-smlz$3h&t7z^ul'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	 'django.template.loaders.filesystem.Loader',
	 'django.template.loaders.app_directories.Loader',
#		'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
	 'django.middleware.common.CommonMiddleware',
	 'django.contrib.sessions.middleware.SessionMiddleware',
	 'django.middleware.csrf.CsrfViewMiddleware',
	 'django.contrib.auth.middleware.AuthenticationMiddleware',
	 'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'cacho.urls'

TEMPLATE_DIRS = (
	 os.path.join(SITE_ROOT, 'templates')
)

INSTALLED_APPS = (
	 'django.contrib.auth',
	 'django.contrib.contenttypes',
	 'django.contrib.sessions',
	 'django.contrib.sites',
	 'django.contrib.messages',
	 'django.contrib.staticfiles',
	 'django.contrib.auth',
	 'cacho_app',
	 'django.contrib.admin',
)

LOGGING = {
	 'version': 1,
	 'disable_existing_loggers': False,
	 'handlers': {
		  'mail_admins': {
				'level': 'ERROR',
				'class': 'django.utils.log.AdminEmailHandler'
		  }
	 },
	 'formaters': {
		  'verbose': {
				'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
		  },
		  'simple': {
				'format': '%(levelname)s %(message)s'
		  }
	 },
	 
	 # 'handlers': {
		#   'console': {
		# 		'level':'DEBUG',
		# 		'class':'logging.StreamHandler',
		# 		'formatter': 'simple'
		#   }
	 # },	
	 'loggers': {
		  'django.request': {
				'handlers': ['mail_admins'],
				'level': 'ERROR',
				'propagate': True,
		  },
		  # 'socketio': {
				# 'handlers':['console'],
				# 'propagate': True,
				# 'level':'INFO',
		  # }
	 }
}
