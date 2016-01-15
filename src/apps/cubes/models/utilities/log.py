from django.db import models


class Log(models.Model):
    """
    Log

    logs registered aggregates for a period and a cube/fact
    """

    cube = models.CharField(max_length=255)
    date = models.DateField(default=None)
    time_taken = models.CharField(max_length=10, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        app_label = 'cubes'
        db_table = 'log'
        unique_together = ('cube', 'date')
