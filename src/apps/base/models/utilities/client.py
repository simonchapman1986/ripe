from django.db import models
from django_extensions.db.fields import UUIDField

import logging

logger = logging.getLogger('reporting')


class Clients(models.Model):
    """
    Clients

    when we ingest our clients, we store their information here. This information can then be used for other processes
    and also to sanity check our incoming events to ensure the client does exist.

    We also use this information to generate some reports (i.e. ftp_client_dir)
    """
    id = UUIDField(version=4, primary_key=True)
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=1024)
    ftp_client_dir = models.CharField(max_length=255, default='default')

    class Meta:
        app_label = 'base'
        db_table = 'clients'
