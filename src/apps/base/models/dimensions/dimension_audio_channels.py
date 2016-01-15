from django.db import models
from dimension import select_or_insert


class DimensionAudioChannels(models.Model):
    """
    DimensionAudioChannels

    """

    channel = models.CharField(max_length=255)

    class Meta:
        app_label = 'base'
        db_table = 'dim_audio_channels'

    @classmethod
    def insert(cls, **kwargs):
        return select_or_insert(cls, values={}, **kwargs)
