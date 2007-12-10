import os, platform
DEVELOPMENT_MODE = (platform.node() != "websushi.org")

ADMINS = (('Jannis Leidel', 'jannis@leidel.info'),)
MANAGERS = ADMINS

if DEVELOPMENT_MODE:
    DEBUG = True
    PREPEND_WWW = False
    CACHE_BACKEND = "file:///tmp/"
    DOCS_SVN_ROOT = "http://svn.django-de.org/"
    DATABASE_ENGINE = 'sqlite3'
    DATABASE_NAME = 'django_de.db'
    SECRET_KEY = 'a1o#rz$vv6i$ptm-86h^r7n@v#v!h-@4+gh1e$@jf+b+li4z$*'
else:
    DEBUG = False
    PREPEND_WWW = True
    try:
        from local_settings import *
    except ImportError:
        pass

DOCS_SVN_PATH = "docs/live/"

TEMPLATE_DEBUG = DEBUG

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'de'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    #'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'django_de.urls'

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIRS = [os.path.join(PROJECT_PATH, 'templates')]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django_de.apps.authors',
    'django_de.apps.documentation',
)
