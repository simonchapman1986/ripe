from django.db import models
from django_extensions.db.fields import UUIDField
from apps.base.models.dimensions.dimension import select_or_insert
from apps.flags.checks.client import client


class DimensionClient(models.Model):
    """
    DimensionClient

    Dim to filter down on clients within the reported data facts

    Although this is merely a dim within the system, we have a flag set to this dim.
    The reason for this is because we ingest clients. If we are receiving events for a client that does not yet
    exist in the clients table, something is going awry, either the ingested data, or one of our events is failing
    to ingest as it should.

    The 'client' flag simply checks the client table upon insertion, if the client does exist, we are ok and no
    flag is required. However if it does not yet exist, there may be an issue so a DoesNotExist flag is raised.

    Regardless of the flag outcome we always store the client dim, we cannot ignore the data we receive.
    """
    client_id = UUIDField(version=4, unique=True)

    class Meta:
        app_label = 'base'
        db_table = 'dim_client'

    @classmethod
    def insert(cls, **kwargs):
        cid = kwargs.get('client_id', False)
        if cid != -1:
            client(client_id=cid, event_name='insert')
        return select_or_insert(cls, values={}, **kwargs)
