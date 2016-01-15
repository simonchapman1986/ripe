from django.db import models

from apps.base.models.dimensions.dimension_utc_date import DimensionUTCDate


class FactServicesHeartbeatPlayBuffer(models.Model):

    duration = models.BigIntegerField(null=False)
    event_time = models.DateTimeField(null=False)
    event_utc_date = models.ForeignKey(DimensionUTCDate, null=True)
    last_modified = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        app_label = 'base'
        db_table = 'fact_services_heartbeat_play_buffer'
