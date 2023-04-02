from .settings import *
DEBUG = True
ALLOWED_HOSTS = []
STATIC_URL = 'static/'

# DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3',
#                          'NAME': os.path.join(BASE_DIR, 'db.sqlite3'), }}

if DEBUG:
    def show_toolbar(request):
        return True

    INSTALLED_APPS += ('debug_toolbar',)
    MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    DEBUG_TOOLBAR_CONFIG = {'SHOW_TOOLBAR_CALLBACK': show_toolbar, }
