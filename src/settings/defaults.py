import os
from celery.schedules import crontab


#######################################
# Settings that have been considered: #
#######################################

# Absolute path of project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', ''))

# Absolute path to the directory report files should be stored in.
REPORTS_ROOT = os.path.join(PROJECT_ROOT, 'reports')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ripe',
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}

CACHES = {
    'default': {
        'CACHE_TYPE': 'memcached',
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'preprod-elasticache.l1l2bg.cfg.usw1.cache.amazonaws.com:11211',
        'BINARY': True,
        'OPTIONS': {
                    'tcp_nodelay': True,
                    'ketama': True
        }
    },
    'health_check': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }

}

UPLOAD_REPORTS = [
    'content',
    'license',
    'transaction',
    'subscription_revenue',
    'registrations-raw',
]

SFTP_SERVER = ''
SFTP_PORT = 22
SFTP_USERNAME = ''
SFTP_PASSWORD = ''
SFTP_HOMEDIR = ''
SFTP_REPORTSDIR = ''
DEFAULT_SFTP_LOCATION = ''


DEFAULT_FTP_PATH = 'home/default/reports/dev'

SFTP_SETTINGS = {
    'DEFAULT': {
        'server': '',
        'port': 22,
        'path': '/home/default/reports/dev',
        'username': '',
        'password': '',
    },
}

SERVICE_SETTINGS = {
    'DEFAULT': {
        'report_filename': '{}_Report_WC_{}.csv'
    },
    'content': {
        'report_filename': '{}_ContentStorageReport_WC_{}.csv'
    },
    'license': {
        'report_filename': '{}_Licenses_WC_{}.csv'
    },
    'transaction': {
        'report_filename': '{}_Transactions_WC_{}.csv'
    },
    'subscription_revenue': {
        'report_filename': '{}_Subscriptions_WC_{}.csv'
    },
    'registrations-raw': {
        'report_filename': '{}_RegisteredUsers_WC_{}.csv'
    }

}

CONTENT_SETTINGS = {
    'upload_server': {
        'server': '',
        'port': 22,
        'path': '/home/default/reports/dev'
    },
    'report_filename': '_ContentStorageReport_WC_',
    'sftp_username': 'reporting',
    'sftp_password': 'shwiHickUc',
    'report_frequency': 'weekly',
}

GEOIP_MAXMIND_LICENSE_KEY = ''
TIME_ZONE = 'UTC'

DATE_FORMAT_YMD = '%Y-%m-%d'
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
CLIENT_UPDATE_TIMEDELTA = 300
SERVICE_UPDATE_TIMEDELTA = 300
SERVICE_MANAGER_INTERNAL_URI = ''
AGGREGATE_FACTS_WHEN = crontab(hour="1")


################################################################
# Settings that MAY have been copied wholesale from elsewhere: #
################################################################

DEBUG = False
TEMPLATE_DEBUG = DEBUG
ADMIN_ENABLED = True
ADMINS = (
    ('Simon Chapman', 's.chapman86@me.com'),
)
MANAGERS = ADMINS
ALLOWED_HOSTS = ['*']
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = ()

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = 'lxc#_emo5m7eonl7a==n1vmaf76v3)*0g)lh8*k!s+_f1ock%d'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.messages.middleware.MessageMiddleware',
    'saffron.api.middleware.RequestExceptionsMiddleware',
    'saffron.api.middleware.RequestParamMiddleware',
)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = ()

BROKER_URL = ""
CELERY_IMPORTS = ("apps.events", "apps.cubes.tasks")
CELERY_RESULT_BACKEND = 'amqp'
CELERY_IGNORE_RESULT = True

import djcelery
djcelery.setup_loader()

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'raven.contrib.django.raven_compat',
    'django.contrib.admin',
    'django_extensions',
    'djcelery',
    'kombu.transport.django',
    'tastypie',
    'apps.base',                            # RIPE core - architecture
    'apps.api',                             # apis - reporting apis
    'apps.bi',                              # business intelligence
    'apps.br',                              # business rules/logic
    'apps.reporting',                       # report generating
    'apps.flags',                           # flags - outcome of a certain flag
    'apps.events',                          # events - our event tasks
    'apps.cubes',                           # cubes - our cube OLAP system
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

import sys
root_handlers = ['local_logging']
reporting_handlers = ['reporting_handler']
if 'test' not in sys.argv and 'jenkins' not in sys.argv:
    root_handlers.append('sentry_handler')
    reporting_handlers.append('sentry_handler')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'functional_format': {
            'format': '%(asctime)s %(name)s %(levelname)s %(funcName)s %(message)s'
        },
    },
    'handlers': {
        'local_logging': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'functional_format',
            'filename': '/var/log/ripe/ripe_root.log'
        },
        'reporting_handler': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'functional_format',
            'filename': '/var/log/ripe/ripe.log'
        },
        'sentry_handler': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.handlers.SentryHandler'
        },
    },
    'loggers': {
        '': {
            'handlers': root_handlers,
            'level': 'DEBUG',
            'propagate': False,
        },
        'reporting': {  # because celery messes with the root logger!!!
            'handlers': reporting_handlers,
            'level': 'DEBUG',
            'propagate': False,
        },
        'requests': {
            'level': 'WARNING',
            'propagate': False,
        }
    }
}

#RAVEN_CONFIG = ''

HEALTH_CHECK = {
    'check_db': True,
    'check_migrations': True,
    'check_disk_space': True,
    'check_services': True,
    'check_access_keys': False,
    'disk_space_locations': {
    },
    'service_locations': {
    }
}

HEALTH_MONITOR = {
    'check_apis': True,
    'check_cpu': True,
    'check_memory': True,
}

RIPE_RESPONSE = {
    'CSV_HEADERS': ['start', 'end', 'name', 'total', 'new',  'average', 'group'],
    'CSV_ROW_FIELD_INDEX': [0, 1, 2],
    'REPORT_PARENT_ELEMENT': 'current_report',
    'REPORT_PARENT_ELEMENT_START_KEY': '0',
}


# - use manual command 'makecsv'. uncomment when all testing/QA done.
# CELERYBEAT_SCHEDULE = {
#     'create-upload-content-storage-report': {
#         'task': 'apps.events.csv_reports.upload.upload_report',
#         'schedule': crontab(hour=1, minute=5, day_of_week='mon')
#     },
# }

# final schedule to be used after int testing/QA
# crontab(hour=1, minute=5, day_of_week='mon')

