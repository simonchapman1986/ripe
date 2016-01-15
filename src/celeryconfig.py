# CELERY_TIMEZONE = 'ETC/UTC'
from celery.schedules import crontab

CELERY_ENABLE_UTC = True

# We're not using rate limits
CELERY_DISABLE_RATE_LIMITS = True

CELERY_IMPORTS = ("apps.events", "apps.cubes.tasks")
# CELERY_IMPORTS = "apps.events"  # for tests

CELERY_RESULT_BACKEND = 'amqp'

# settings for test for now.
CELERYD_MAX_TASKS_PER_CHILD = 1



